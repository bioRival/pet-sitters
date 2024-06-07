from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        label='E-mail',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Почта'
        })
    )
    password = forms.CharField(
        max_length=128,
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'password']


class RegistrationForm(UserCreationForm):
    PACKAGES = [
        ('заказчик', 'Я - клиент'),
        ('исполнитель', 'Я - ситтер'),
    ]

    username = forms.CharField(
        max_length=150,
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email'
        })
    )
    password1 = forms.CharField(
        max_length=128,
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )

    user_type = forms.ChoiceField(choices=PACKAGES, widget=forms.Select())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', ]

