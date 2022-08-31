from django.contrib import admin

# Register your models here.
from .models import BankAccount, Transaction, BankOption

admin.site.register(BankAccount)
admin.site.register(BankOption)
admin.site.register(Transaction)

class TransactionAdmin(admin.ModelAdmin):
    class Meta:
        model = Transaction
        fields = '__all__'
        readonly_fields = ('id', )