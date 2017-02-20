from django.contrib import admin
from . import models

admin.site.register(models.Accounts)
admin.site.register(models.Categories)
admin.site.register(models.Balance)
