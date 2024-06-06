from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from core.models import Customer
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


# class CustomRegistrationView(CreateView):
#     form_class = RegistrationForm
#     template_name = 'user_app/signup.html'
#     extra_context = {'title': 'Регистрация на сайте'}
#
#     def get_success_url(self):
#         return reverse_lazy('user_app:login')
#
#     def form_valid(self, form):
#         user = form.save()
#         return super().form_valid(form)


def customer_signup(request):
    if request.method == "POST":
        username = request.POST['email']
        first_name = request.POST['first_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        # password2 = request.POST['password2']
        user_type = request.POST['user_type']

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Этот e-mail уже занят.')
            return redirect('/user/signup')

        # if password1 != password2:
        #     messages.error(request, "Неправильный пароль.")
        #     return redirect('/customer_signup')

        user = User.objects.create_user(username=username, first_name=first_name,
                                        password=password1, email=email)
        customers = Customer.objects.create(user=user, user_type=user_type)

        # user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
        #                                 password=password1, email=email)
        # customers = Customer.objects.create(user=user, phone=phone, location=location, image=image, user_type=user_type)
        user.save()
        customers.save()
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
