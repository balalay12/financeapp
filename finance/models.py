from django.db import models

OPERATIONS_TYPE = (
    ('I', 'Доход'),
    ('C', 'Расход')
)


class Categories(models.Model):
    name = models.CharField(max_length=250)
    operation_type = models.CharField(
        max_length=1, choices=OPERATIONS_TYPE, default='C')

    def __str__(self):
        return self.name


class Accounts(models.Model):
    STATUS = (
        ('I', 'Не используется'),
        ('A', 'Используется')
    )

    owner = models.ForeignKey('auth.User')
    name = models.CharField(max_length=250)
    score = models.FloatField()
    status = models.CharField(max_length=1, choices=STATUS, default='A')


class Balance(models.Model):
    date = models.DateField()
    operation = models.CharField(max_length=1, choices=OPERATIONS_TYPE)
    amount = models.FloatField()
    category = models.ForeignKey(Categories)
    user = models.ForeignKey('auth.User')
    account = models.ForeignKey(Accounts, null=True)
