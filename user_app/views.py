from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

from django.core.mail import send_mail
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from core.models import Customer, Pet, Service
from user_app import forms
from user_app.forms import LoginForm


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


# регистрация пользователя
def customer_signup(request):
    if request.method == "POST":
        username = request.POST['email']
        first_name = request.POST['first_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        user_type = request.POST['user_type']

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Этот e-mail уже занят.')
            return redirect('/user/signup')

        user = User.objects.create_user(username=username, first_name=first_name,
                                        password=password1, email=email)
        customer = Customer.objects.filter(user=user).update(user_type=user_type)

        send_mail(
            subject='Регистрация пройдена успешно',
            message=f'Здравствуйте! Вы успешно зарегистрированы на сайте petsitters.ru.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        username = request.POST['email']
        password = request.POST['password1']
        user = authenticate(username=username, password=password)
        login(request, user)

        return HttpResponseRedirect('/')
    return render(request, "user_app/signup.html")


# страница профиля заказчика
class CustomerProfileView(TemplateView):
    template_name = 'user_app/custom_profile_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user = get_object_or_404(User, username=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404("Пользователь не найден")
        context['customer_profile'] = user
        context['customer_pets'] = Pet.objects.filter(host=user)
        context['title'] = f'Профиль пользователя {user}'
        return context


# смена пароля
class UserSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'user_app/profile_settings_page.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user == get_object_or_404(User, username=self.kwargs.get('username')):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise HttpResponseForbidden("Вы не имеете доступа к этой странице.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_password_form'] = forms.UserPasswordForm(self.request.user)
        context['title'] = f'Настройки профиля {self.request.user}'
        return context

    def post(self, request, *args, **kwargs):
        if 'user_password_form' in request.POST:
            form = forms.UserPasswordForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Пароль успешно изменён.')
                return self.get(request, *args, **kwargs)
            else:
                context = self.get_context_data(**kwargs)
                context['user_password_form'] = form
                return render(request, self.template_name, context)

        else:
            return self.get(request, *args, **kwargs)


# редактирование профиля
class UserEditView(LoginRequiredMixin, TemplateView):
    template_name = 'user_app/profile_edit_page.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user == get_object_or_404(User, username=self.kwargs.get('username')):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise HttpResponseForbidden("Вы не имеете доступа к этой странице.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_info_form'] = forms.CustomInfoForm(instance=self.request.user)
        context['user_profile_form'] = forms.ProfileForm(instance=self.request.user.profile)
        context['title'] = f'Настройки профиля {self.request.user}'
        return context

    def post(self, request, *args, **kwargs):
        if 'user_info_form' in request.POST:
            user_info_form = forms.CustomInfoForm(request.POST, instance=request.user)
            user_profile_form = forms.ProfileForm(request.POST, request.FILES, instance=self.request.user.profile)
            if user_info_form.is_valid() and user_profile_form.is_valid():
                user_info_form.save()
                user_profile_form.save()
                messages.success(request, 'Данные успешно изменены.')
                return redirect('user_app:customer_profile', user_info_form.cleaned_data.get('username'))
            else:
                context = self.get_context_data(**kwargs)
                context['user_info_form'] = user_info_form
                context['user_profile_form'] = user_profile_form
                return render(request, self.template_name, context)


# страница профиля ситтера
class SitterProfileView(TemplateView):
    template_name = 'user_app/sitter_profile_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user = get_object_or_404(User, username=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404("Пользователь не найден")
        context['sitter_profile'] = user
        context['sitter_services'] = Service.objects.filter(sitter=user)
        context['title'] = f'Профиль пользователя {user}'
        return context


# редактирование профиля ситтера
class SitterEditView(LoginRequiredMixin, TemplateView):
    template_name = 'user_app/sitter_edit_page.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user == get_object_or_404(User, username=self.kwargs.get('username')):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise HttpResponseForbidden("Вы не имеете доступа к этой странице.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_info_form'] = forms.CustomInfoForm(instance=self.request.user)
        context['user_profile_form'] = forms.ProfileForm(instance=self.request.user.profile)
        context['sitter_profile_form'] = forms.SitterProfileForm(instance=self.request.user.profile)
        context['title'] = f'Настройки профиля {self.request.user}'
        return context

    def post(self, request, *args, **kwargs):
        if 'user_info_form' in request.POST:
            user_info_form = forms.CustomInfoForm(request.POST, instance=request.user)
            user_profile_form = forms.ProfileForm(request.POST, request.FILES, instance=self.request.user.profile)
            sitter_profile_form = forms.SitterProfileForm(request.POST, request.FILES, instance=self.request.user.profile)

            if user_info_form.is_valid() and user_profile_form.is_valid() and sitter_profile_form.is_valid():
                user_info_form.save()
                user_profile_form.save()
                sitter_profile_form.save()
                messages.success(request, 'Данные успешно изменены.')
                return redirect('user_app:sitter_profile', user_info_form.cleaned_data.get('username'))
            else:
                context = self.get_context_data(**kwargs)
                context['user_info_form'] = user_info_form
                context['user_profile_form'] = user_profile_form
                context['sitter_profile_form'] = sitter_profile_form
                return render(request, self.template_name, context)
