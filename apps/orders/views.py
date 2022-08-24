from django.db import transaction

from rest_framework.response import Response
from rest_framework import views
from rest_framework import status

from apps.orders.models import Order, OrderItem
from apps.cart.models import CartItem
from apps.products.models import ProductInventory
from apps.orders import serializers
from apps.orders import utils

# Create your views here.
class PlaceTheOrder(views.APIView):
    def post(self, request):
        cart_items = CartItem.objects.filter(user__id = request.user.id)
        request.data['store'] = cart_items[0].product.store.id
        request.data['user'] = request.user.id
        
        with transaction.atomic():
            serializer = serializers.OrderSerializer(data = request.data)
            if serializer.is_valid(raise_exception=True):
                order =serializer.save()

            total_price = 0

            for item in cart_items:
                product_inventory = ProductInventory.objects.get(id = item.product.id)

                if utils.cart_quantity_lt_remaining_units(item, product_inventory):
                    price = utils.calc_price(item, product_inventory)

                    order_item_params = {
                        'order' : order.id,
                        'product' : item.product.id,
                        'quantity': item.quantity,
                        'price' : price
                    }

                total_price += price
                serializer = serializers.OrderItemSerializer(data = order_item_params)
                
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

            order.total_price = total_price
            order.save()
        
            cart_items.delete()

            return Response(f'''Your Order Request Sent.\n
                                \tOrder ID: {order.id}\n
                                \tTotal Bill:{total_price}\n
                                \tPlease Complete The Payment Process''',
                                status= status.HTTP_200_OK)