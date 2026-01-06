from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, View
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm


class RegisterView(FormView):
    """Регистрация с перенаправлением в каталог"""

    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(
            self.request,
            f'Регистрация успешно завершена! Добро пожаловать, {user.email}!'
        )

        return super().form_valid(form)


class CustomLoginView(LoginView):
    """Вход с перенаправлением в каталог"""

    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('catalog:home')

    def form_valid(self, form):
        messages.success(
            self.request,
            f'Добро пожаловать, {form.get_user().email}!'
        )
        return super().form_valid(form)


class CustomLogoutView(View):
    """Выход с перенаправлением в каталог"""

    def get(self, request):
        logout(request)
        messages.info(request, 'Вы успешно вышли из системы.')
        return redirect('catalog:home')
