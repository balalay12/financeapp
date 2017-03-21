import datetime
from dateutil.relativedelta import relativedelta
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import ListView
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from . import forms, models


class CheckAuth(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        return super(CheckAuth, self).dispatch(request, *args, **kwargs)


class CheckAccountOwner(CheckAuth):
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.owner == request.user:
            return HttpResponseForbidden()
        return super(CheckAccountOwner, self).dispatch(
            request, *args, **kwargs)


class CheckBalanceUser(CheckAuth):
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.user == request.user:
            return HttpResponseForbidden()
        return super(CheckBalanceUser, self).dispatch(request, *args, **kwargs)


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
    date = datetime.date.today()

    def get_queryset(self):
        self.accounts = models.Accounts.objects.filter(
            owner=self.request.user.id)
        if self.request.GET.get('prev', False):
            self.date = datetime.datetime.strptime(
                self.request.GET['date'], '%Y-%m-%d') - relativedelta(months=+1)
        if self.request.GET.get('next', False):
            self.date = datetime.datetime.strptime(
                self.request.GET['date'], '%Y-%m-%d') + relativedelta(months=+1)
        self.balance = models.Balance.objects.filter(
            user=self.request.user.id,
            date__month=self.date.month,
            date__year=self.date.year)

    def get_context_data(self, **kwargs):
        ctx = super(Index, self).get_context_data(**kwargs)
        ctx['accounts'] = self.accounts
        ctx['accounts_sum'] = self.accounts.filter(
            status='A').aggregate(Sum('score'))
        ctx['balance'] = self.balance
        ctx['total_cost'] = self.balance.filter(
            operation='C').aggregate(
            Sum('amount'))
        ctx['total_incom'] = self.balance.filter(
            operation='I').aggregate(Sum('amount'))
        ctx['today'] = self.date
        return ctx


class AccountsCreate(CheckAuth, CreateView):
    model = models.Accounts
    fields = ('name', 'score')
    success_url = '/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(AccountsCreate, self).form_valid(form)


class AccountUpdate(CheckAccountOwner, UpdateView):
    model = models.Accounts
    fields = ['name', 'score']
    template_name = 'forms/accounts_update_form.jinja2'
    success_url = '/'


class AccountDelete(CheckAuth, RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        account = models.Accounts.objects.get(pk=kwargs['pk'])
        if account.owner is not request.user:
            return HttpResponseForbidden()
        account.status = 'I'
        account.save()
        return super(AccountDelete, self).get(request, *args, **kwargs)


class BalanceCreate(CheckAuth, CreateView):
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


class BalanceUpdate(CheckBalanceUser, UpdateView):
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


class BalanceDelete(CheckBalanceUser, DeleteView):
    model = models.Balance
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        balance = self.get_object()
        if balance.operation == 'C':
            balance.account.score += balance.amount
        else:
            balance.account.score -= balance.amount
        balance.account.save()
        return super(BalanceDelete, self).delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
