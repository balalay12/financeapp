from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Balance


class BalanceForm(ModelForm):
    class Meta:
        model = Balance
        fields = ('date', 'amount', 'category', 'account', 'operation')

    def clean(self):
        cleaned_data = super(BalanceForm, self).clean()
        account = cleaned_data['account']
        amount = cleaned_data['amount']
        if cleaned_data['operation'] == 'C':
            if account.score < amount:
                raise ValidationError('Недостаточная сумма на счету')
            account.score -= amount
            account.save()
        else:
            account.score += amount
            account.save()
        return cleaned_data


class BalanceUpdateForm(ModelForm):
    class Meta:
        model = Balance
        fields = ('date', 'amount', 'category', 'account', 'operation')

    def clean(self):
        cleaned_data = super(BalanceUpdateForm, self).clean()
        account = cleaned_data['account']
        amount = cleaned_data['amount']
        if cleaned_data['operation'] == 'C':
            if account.id is not self.instance.account.id:
                if account.score < amount:
                    raise ValidationError('Недостаточная сумма на счету')
                self.instance.account.score += self.instance.amount
                account.score -= amount
                self.instance.account.save()
                account.save()
            else:
                if amount > self.instance.amount:
                    if account.score - amount <= 0:
                        raise ValidationError('Недостаточная сумма на счету')
                    account.score -= (amount - self.instance.amount)
                    account.save()
                else:
                    print(self.instance.amount - amount)
                    account.score += (self.instance.amount - amount)
                    account.save()
        if cleaned_data['operation'] == 'I':
            if account.id is not self.instance.account.id:
                self.instance.account.score -= self.instance.amount
                account.score += amount
                self.instance.account.save()
                account.save()
            else:
                if amount > self.instance.amount:
                    account.score -= (self.instance.amount - amount)
                    account.save()
                else:
                    account.score += (amount - self.instance.amount)
                    account.save()
        return cleaned_data
