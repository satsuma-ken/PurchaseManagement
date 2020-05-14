from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import(LoginView, LogoutView)
from django.views import generic
from .forms import LoginForm

class Top(generic.TemplateView):
    template_name = 'login/top.html'

class Login(LoginView):
    form_class = LoginForm
    template_name = 'login/login.html'

class Logout(LogoutView):
    template_name = 'login/top.html'
