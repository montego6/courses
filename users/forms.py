from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
    label="Введите пароль",
    strip=False,
    widget=forms.PasswordInput,
    help_text=password_validation.password_validators_help_text_html(),
)    
    password2 = forms.CharField(
    label="Подтвердите пароль",
    strip=False,
    widget=forms.PasswordInput,
    help_text=password_validation.password_validators_help_text_html(),
)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Имя пользователя',
            'first_name': 'Ваше имя',
            'last_name': 'Ваша фамилия',
            'email': 'Электронная почта',
        }


    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     if commit:
    #         user.save()
    #     return user