from django.db import models

from django.conf import settings
from apps.products.models import ProductInventory


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart', default= 1)
    product = models.ForeignKey(ProductInventory, related_name='cart_items',
                                on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name} , quantity: {self.quantity}'

