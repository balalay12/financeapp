.import datetime
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.views.generic import ListView
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from . import forms, models


class UserLogin(FormView):
    template_name = 'forms/login.jinja2'
    form_class = AuthenticationForm
    success_url = '/'

    def form_valid(self, form):
        if form.get_user():
            login(self.request, form.get_user())
            return super(UserLogin, self).form_valid(form)


class UserRegistration(FormView):
    template_name = 'forms/reg.jinja2'
    form_class = UserCreationForm
    success_url = '/login/'

    def form_valid(self, form):
        form.save()
        return super(UserRegistration, self).form_valid(form)


class UserLogout(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(UserLogout, self).get(request, *args, **kwargs)


class Index(ListView):
    template_name = 'index.jinja2'
    accounts = {}
    balance = {}

    def get_queryset(self):
        self.accounts = models.Accounts.objects.filter(owner=self.request.user.id)
        self.balance = models.Balance.objects.filter(user=self.request.user.id)

    def get_context_data(self, **kwargs):
        ctx = super(Index, self).get_context_data(**kwargs)
        ctx['accounts'] = self.accounts
        ctx['accounts_sum'] = self.accounts.filter(status='A').aggregate(Sum('score'))
        ctx['balance'] = self.balance
        ctx['total_cost'] = self.balance.filter(
            operation='C',
            date__month=datetime.date.today().month,
            date__year=datetime.date.today().year).aggregate(Sum('amount'))
        ctx['total_incom'] = self.balance.filter(
            operation='I',
            date__month=datetime.date.today().month,
            date__year=datetime.date.today().year).aggregate(Sum('amount'))
        return ctx


class AccountsCreate(CreateView):
    model = models.Accounts
    fields = ('name', 'score')
    success_url = '/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(AccountsCreate, self).form_valid(form)


class AccountUpdate(UpdateView):
    model = models.Accounts
    fields = ['name', 'score']
    template_name = 'forms/accounts_update_form.jinja2'
    success_url = '/'


class AccountDelete(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        account = models.Accounts.objects.get(pk=kwargs['pk'])
        account.status = 'I'
        account.save()
        return super(AccountDelete, self).get(request, *args, **kwargs)


class BalanceCreate(CreateView):
    model = models.Balance
    template_name = 'forms/balance_new_form.jinja2'
    success_url = '/'
    form_class = forms.BalanceForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BalanceCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(BalanceCreate, self).get_context_data(**kwargs)
        ctx['categories'] = models.Categories.objects.filter(
            operation_type=self.request.GET['type'])
        ctx['accounts'] = models.Accounts.objects.filter(
            owner=self.request.user.id,
            status='A')
        return ctx


class BalanceUpdate(UpdateView):
    model = models.Balance
    form_class = forms.BalanceUpdateForm
    success_url = '/'
    template_name = 'forms/balance_update_form.jinja2'

    def get_context_data(self, **kwargs):
        ctx = super(BalanceUpdate, self).get_context_data(**kwargs)
        ctx['accounts'] = models.Accounts.objects.filter(
            owner=self.request.user.id,
            status='A')
        ctx['categories'] = models.Categories.objects.filter(
            operation_type=self.request.GET['type'])
        return ctx


class BalanceDelete(DeleteView):
    model = models.Balance
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        balance = models.Balance.objects.get(pk=kwargs['pk'])
        if balance.operation == 'C':
            balance.account.score += balance.amount
        else:
            balance.account.score -= balance.amount
        balance.account.save()
        return super(BalanceDelete, self).delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
