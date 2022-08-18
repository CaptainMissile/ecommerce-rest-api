from django.db import models

from django.conf import settings

from apps.accounts.models import User

class BankOption(models.Model):
    key = models.CharField(max_length=100, primary_key=True)
    value = models.PositiveBigIntegerField()

    def __str__(self):
        return f'({self.key}, {self.value})'


class BankAccount(models.Model):
    account_no = models.PositiveBigIntegerField(unique=True,primary_key=True)
    balance = models.DecimalField(max_digits=10, decimal_places=3, default= 0)
    credential = models.CharField(max_length=100)

    def __str__(self):
        return str(self.account_no)
    

class Transaction(models.Model):
    TRANSACTION_STATUS_CHOICES = (
        ('P', 'Pending'),
        ('A', 'Approved'),
    )

    TRANSACTION_TYPE_CHOICES = (
        ('I', 'Cash In'),
        ('S', 'Send To'),
    )

    account_from = models.ForeignKey(BankAccount, related_name='transaction_from', on_delete = models.PROTECT, blank=True, null=True)
    credential = models.CharField(max_length=100, blank=True, null=True)

    account_to = models.ForeignKey(BankAccount, related_name='transaction_to', on_delete = models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    status = models.CharField(choices=TRANSACTION_STATUS_CHOICES, default='P', max_length= 1)
    type = models.CharField(choices=TRANSACTION_TYPE_CHOICES, max_length= 1)

    created_at = models.DateTimeField(auto_now_add = True, editable=False)
    
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True, on_delete = models.PROTECT)

    def __str__(self):
        return f'TYPE: {self.type} -- Amount:{self.amount}, (From: {self.account_from}, To: {self.account_to})'