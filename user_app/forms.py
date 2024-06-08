from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from core import models


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


class CustomInfoForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        label='Имя пользователя (username)',
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
    first_name = forms.CharField(
        max_length=150,
        label='Имя',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше имя'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        label='Фамилия',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите вашу фамилию'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UserPasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        max_length=128,
        label='Старый пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите старый пароль'
        })
    )
    new_password1 = forms.CharField(
        max_length=128,
        label='Новый пароль',
        help_text=password_validation.password_validators_help_text_html(),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите новый пароль'
        })
    )
    new_password2 = forms.CharField(
        max_length=128,
        label='Подтверждение нового пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите новый пароль'
        })
    )


class ProfileForm(forms.ModelForm):
    image = forms.FileField(
        label='Аватарка',
        required=False,
        widget=forms.FileInput(
            attrs={
                'type': 'file',
                'class': 'form-control',
            }
        )
    )

    phone = forms.CharField(
        max_length=12,
        label='Телефон',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите номер телефона'
        })
    )

    location = forms.CharField(
        max_length=254,
        label='Город',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите свой город'
        })
    )

    show_email = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input mt-0',
            }
        )
    )

    show_phone = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input mt-0'
            }
        )
    )

    class Meta:
        model = models.Customer
        fields = ['image', 'phone', 'location', 'show_email', 'show_phone']
