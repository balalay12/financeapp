from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . import forms


class UserLogin(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = '/'

    def form_valid(self, form):
        if form.get_user():
            login(self.request, form.get_user())
            return super(UserLogin, self).form_valid(form) 


class UserRegistration(FormView):
    template_name = 'reg.html'
    form_class = UserCreationForm
    success_url = '/login/'

    def form_valid(self, form):
        form.save()
        return super(UserRegistration, self).form_valid(form)
