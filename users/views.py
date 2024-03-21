from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from users.forms import LoginUserForm


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found 404</h1> <a href='/'>На главную страницу</a>")


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('documents:list')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('users:login'))


class Settings(TemplateView):
    template_name = 'users/settings.html'
    extra_context = {'title': 'Настройки'}