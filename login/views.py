from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import(LoginView, LogoutView)
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect, resolve_url
from django.template.loader import render_to_string
from django.views import generic
from .forms import (LoginForm, UserCreateForm, UserUpdateForm)

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
        # subject = 'yahoo'
        # message = 'google'

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