from wsgiref.simple_server import demo_app
from django.db import models

# Create your models here.
from apps.orders.models import Order
from apps.bank.models import Transaction

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete = models.CASCADE)
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    is_checked = models.BooleanField(default=False)