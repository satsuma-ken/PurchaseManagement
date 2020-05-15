from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import(
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.core.mail import send_mail
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect, resolve_url
from django.template.loader import render_to_string
from django.views import generic
from django.urls import reverse_lazy
from .forms import (
    LoginForm, UserCreateForm, UserUpdateForm, MyPasswordChangeForm,
    MyPasswordResetForm, MySetPasswordForm, EmailChangeForm
)

User = get_user_model()

class Top(generic.TemplateView):
    template_name = 'login/top.html'

class Login(LoginView):
    form_class = LoginForm
    template_name = 'login/login.html'

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url('login:top')

class Logout(LogoutView):
    template_name = 'login/top.html'

class UserCreate(generic.CreateView):
    template_name = 'login/user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('login/subject.txt', context)
        message = render_to_string('login/message.txt', context)

        user.email_user(subject, message)
        return redirect('login:user_create_done')

class UserCreateDone(generic.TemplateView):
    template_name = 'login/user_create_done.html'

class UserCreateComplete(generic.TemplateView):
    template_name = 'login/user_create_complete.html'
    timeout_seconds = getattr(settings,'ACTIVATION_TIMEOUT_SECONDS', 60 * 60 * 24)

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        except SignatureExpired:
            return HttpResponseBadRequest()

        except BadSignature:
            return HttpResponseBadRequest()

        else:
            try:
                user = User.objects.get(pk=user_pk)
                
            except User.DoesNotExist:
                return HttpResponseBadRequest()

            else:
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()

class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True
    
    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser

class UserDetail(OnlyYouMixin, generic.DetailView):
    model = User
    template_name = 'login/user_detail.html'

class UserUpdate(OnlyYouMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'login/user_update.html'

    def get_success_url(self):
        return resolve_url('login:user_detail', pk=self.kwargs['pk'])

class PasswordChange(PasswordChangeView):
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('login:password_change_done')
    template_name = 'login/password_change.html'

class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'login/password_change_done.html'

class PasswordReset(PasswordResetView):
    subject_template_name = 'login/reset_subject.txt'
    message_template_name = 'login/reset_message.txt'
    template_name = 'login/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('login:password_reset_done')

class PasswordResetDone(PasswordResetDoneView):
    template_name = 'login/password_reset_done.html'

class PasswordResetConfirm(PasswordResetConfirmView):
    form_class = MySetPasswordForm
    success_url = reverse_lazy('login:password_reset_complete')
    template_name = 'login/password_reset_confirm.html'

class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'login/password_reset_complete.html'

class EmailChange(LoginRequiredMixin, generic.FormView):
    template_name = 'login/email_change_form.html'
    form_class = EmailChangeForm

    def form_valid(self, form):
        user = self.request.user
        new_email = form.cleaned_data['email']

        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(new_email),
            'user': user,
        }

        subject = render_to_string('login/email_change_subject.txt', context)
        message = render_to_string('login/email_change_message.txt', context)
        send_mail(subject, message, None, [new_email])

        return redirect('login:email_change_done')

class EmailChangeDone(LoginRequiredMixin, generic.TemplateView):
    template_name = 'login/email_change_done.html'

class EmailChangeComplete(LoginRequiredMixin, generic.TemplateView):
    template_name = 'login/email_change_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            new_email = loads(token, max_age=self.timeout_seconds)

        except SignatureExpired:
            return HttpResponseBadRequest()

        except BadSignature:
            return HttpResponseBadRequest()

        else:
            User.objects.filter(email=new_email, is_active=False).delete()
            request.user.email = new_email
            request.user.save()
            return super().get(request, **kwargs)