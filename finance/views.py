from django.views.generic.edit import FormView
from django.contrib.auth import login
from . import forms

class UserLogin(FormView):
    template_name = 'login.html'
    form_class = forms.LoginForm
    success_url = '/'

    def form_valid(self, form):
        if form.get_user():
            login(self.request, form.get_user())
            return super(UserLogin, self).form_valid(form) 


class UserRegistration(FormView):
    tempalte_name = 'reg.html'
    form_class = forms.RegForm