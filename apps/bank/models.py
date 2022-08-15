from django.db import models

from django.conf import settings

from apps.accounts.models import User


class BankAccount(models.Model):
    account_owner = models.ForeignKey(User, on_delete= models.CASCADE, related_name='bank_account_owner')
    account_no = models.PositiveBigIntegerField(unique=True,primary_key=True)
    balance = models.DecimalField(max_digits=10, decimal_places=3, default= 0)
    credential = models.CharField(max_length=100)
    

class Transaction(models.Model):
    TRANSACTION_STATUS_CHOICES = (
        ('P', 'Pending'),
        ('A', 'Approved'),
    )

    TRANSACTION_TYPE_CHOICES = (
        ('I', 'Cash In'),
        ('S', 'Send To'),
    )

    account_from = models.ForeignKey(BankAccount, related_name='transaction_from', on_delete = models.PROTECT)
    account_to = models.ForeignKey(BankAccount, related_name='transaction_to', on_delete = models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    status = models.CharField(choices=TRANSACTION_STATUS_CHOICES, max_length= 1)
    type = models.CharField(choices=TRANSACTION_TYPE_CHOICES, max_length= 1)

    created_at = models.DateTimeField(auto_now_add = True, editable=False)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True, on_delete = models.PROTECT)