from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Sum
from django.views.generic import ListView
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from . import forms, models


class UserLogin(FormView):
    template_name = 'login.jinja2'
    form_class = AuthenticationForm
    success_url = '/'

    def form_valid(self, form):
        if form.get_user():
            login(self.request, form.get_user())
            return super(UserLogin, self).form_valid(form)


class UserRegistration(FormView):
    template_name = 'reg.jinja2'
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
        ctx['accounts_sum'] = self.accounts.aggregate(Sum('score'))
        ctx['balance'] = self.balance
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
    template_name = 'accounts_update_form.jinja2'
    success_url = '/'


class AccountDelete(DeleteView):
    model = models.Accounts
    success_url = '/'


class BalanceCreate(CreateView):
    model = models.Balance
    # fields = ('date', 'operation', 'amount', 'category', 'account')
    template_name = 'balance_new_form.jinja2'
    success_url = '/'
    form_class = forms.BalanceForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        # account = form.cleaned_data['account']
        # amount = form.cleaned_data['amount']
        # if account.score < amount:
        #     raise ValidationError('Недостаточная сумма на счету')
        # if form.cleaned_data['operation'] == 'C':
        #     account.score -= amount
        #     account.save()
        return super(BalanceCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(BalanceCreate, self).get_context_data(**kwargs)
        ctx['categories'] = models.Categories.objects.all()
        ctx['accounts'] = models.Accounts.objects.filter(owner=self.request.user.id)
        return ctx
