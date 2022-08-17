from django.contrib import admin

# Register your models here.
from .models import BankAccount, Transaction, BankOption

admin.site.register(BankAccount)
admin.site.register(BankOption)
admin.site.register(Transaction)