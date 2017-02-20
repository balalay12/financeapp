# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

    def clean(self):
        # cleaned_data = super(LoginForm, self).clean()
        if not self.errors:
            user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
            if user is None:
                raise forms.ValidationError('Имя пользователя и пароль не подходят')
            self.user = user
        return cleaned_data

    def get_user(self):
        return self.user or None

class RegForm(forms.Form):
    pass