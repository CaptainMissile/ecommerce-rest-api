from rest_framework.response import Response
from rest_framework import views

from apps.orders.models import Order, OrderItem
from apps.cart.models import CartItem
from apps.products.models import ProductInventory
from apps.orders import serializers
# Create your views here.

def calc_price(item):
    return item.quantity* ProductInventory.price

def cart_quantity_lt_remaining_units(cart_data, product_inventory):
    if cart_data.quantity > 0 and cart_data.quantity <= product_inventory.units:
        return True


class PlaceTheOrder(views.APIView):
    def post(request):
        serializer = serializers.OrderSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            order =serializer.save()

        cart_items = CartItem.objects.filter(user__id = request.user.id)
        for item in cart_items:
            product_inventory = ProductInventory.objects.get(id = item.product.id)
            if cart_quantity_lt_remaining_units(item, product_inventory):
                order_item_params = {
                    'order' : order.id,
                    'product' : item.product.id,
                    'quantity': item.quantity,
                    'price' : calc_price(item, product_inventory)
                }

            OrderItem.objects.create(order_item_params)
        

        cart_items.delete()