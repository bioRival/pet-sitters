from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from user_app.forms import LoginForm, RegistrationForm


class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'user_app/login.html'
    extra_context = {'title': 'Авторизация на сайте'}

    def get_success_url(self):
        return reverse_lazy('home')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class CustomRegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'user_app/signup.html'
    extra_context = {'title': 'Регистрация на сайте'}

    def get_success_url(self):
        return reverse_lazy('user_app:login')

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)
