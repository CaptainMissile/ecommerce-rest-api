from django.db import models

from decimal import Decimal

from django.conf import settings
from apps.products.models import ProductInventory
from apps.store.models import Store

class Order(models.Model):
    BILLING_STATUS_CHOICES = (
        ('P', 'Paid'),
        ('U', 'Unpaid')
    )

    DELIVERY_STATUS_CHOICES = (
        ('P', 'Pending'),
        ('OR', 'Order Registered'),
        ('OW', 'On The Way'),
        ('RC', 'Received By Customer')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='orders')
    full_name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    post_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=7, decimal_places=2, blank =True, null = True)
    billing_status = models.CharField(choices=BILLING_STATUS_CHOICES, max_length=1, default='U')
    delivery_status = models.CharField(choices=DELIVERY_STATUS_CHOICES, max_length=2, default='P')

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(ProductInventory, related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)