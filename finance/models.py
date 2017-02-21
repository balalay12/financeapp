from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Accounts(models.Model):
    owner = models.ForeignKey('auth.User')
    name = models.CharField(max_length=250)
    score = models.FloatField()


class Balance(models.Model):
    OPERATIONS_TYPE = (
        ('I', 'Income'),
        ('C', 'Costs')
    )

    date = models.DateField()
    operation = models.CharField(max_length=1, choices=OPERATIONS_TYPE)
    amount = models.FloatField()
    category = models.ForeignKey(Categories)
    user = models.ForeignKey('auth.User')
    account = models.ForeignKey(Accounts, null=True)
