from django.db import transaction

from rest_framework.response import Response
from rest_framework import views, generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.orders.models import Order, OrderItem
from apps.cart.models import CartItem
from apps.products.models import ProductInventory
from apps.orders import serializers
from apps.orders import utils
from apps.orders.permissions import (IsAllowedToTrackOrder,
                                        IsAllowedToChangeOrderStatus)

# Create your views here.
class PlaceTheOrder(generics.GenericAPIView):
    serializer_class = serializers.PlaceOrderSerializer
    permission_classes = [IsAuthenticated]

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
                print(product_inventory.id,product_inventory.price)
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

            return Response({'msg' : 'Your Order Request Sent.Please Complete The Payment Process.',
                             'order_id': order.id,
                             'total_bill': total_price}, status= status.HTTP_200_OK)

class TrackOrder(views.APIView):
    permission_classes = [IsAuthenticated, IsAllowedToTrackOrder]

    def get(self, request, order_id):
        order = Order.objects.get(id = order_id)
        self.check_object_permissions(request, order)

        serializer = serializers.OrderSerializer(order)

        return Response(serializer.data, status= status.HTTP_200_OK)


class TrackOrderList(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == 4:
            orders = Order.objects.filter(user__id = request.user.id)
        elif request.user.role == 3 :
            orders = Order.objects.filter(store__owner__id = request.user.id)
        elif request.user.role == 3:
            orders = Order.objects.all()
        

        serializer = serializers.OrderSerializer(orders, many=True)

        return Response(serializer.data, status= status.HTTP_200_OK)


class OrderItemList(views.APIView):
    permission_classes = [IsAuthenticated, IsAllowedToTrackOrder]

    def get(self, request, order_id):
        order = Order.objects.get(id = order_id)
        self.check_object_permissions(request, order)
        order_items = OrderItem.objects.filter(order__id = order_id)

        serializer = serializers.OrderItemSerializer(order_items, many=True)

        return Response(serializer.data, status= status.HTTP_200_OK)


class ChangeOrderStatus(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAllowedToChangeOrderStatus]
    serializer_class = serializers.ChangeOrderSerializer

    def post(self,request,order_id):
        data = request.data
        order_instance = Order.objects.get(id = order_id)

        serializer = serializers.ChangeOrderSerializer(instance = order_instance,
                                                        data = data,
                                                        partial=True)

        if serializer.is_valid(raise_exception=True):
            s = serializer.save()

            serializer = serializers.OrderSerializer(s)

            return Response(serializer.data, status= status.HTTP_200_OK)

        
        return Response({'error' : "Order Status is not Changed"},
                            status = status.HTTP_200_OK)
