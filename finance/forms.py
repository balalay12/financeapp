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
            print(account.score)
            account.score -= amount
            account.save()
        else:
            account.score += amount
            account.save()
        return cleaned_data
