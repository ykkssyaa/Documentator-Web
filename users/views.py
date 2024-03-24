from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from users.forms import LoginUserForm


def page_not_found(request, exception):
    return render(request, 'users/404.html', status=404)


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


class ForbiddenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        from django.core.exceptions import PermissionDenied
        if isinstance(exception, PermissionDenied):
            return render(request, 'users/403.html', status=403)