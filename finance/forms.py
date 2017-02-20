# -*- coding: utf-8 -*-

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Пожалуйста введите корректные данные пользователя.",
        'inactive': "Этот пользователь не активен.",
    }


class RegForm(UserCreationForm):
    error_messages = {
        'password_mismatch': "Пароли не совпадают.",
    }
