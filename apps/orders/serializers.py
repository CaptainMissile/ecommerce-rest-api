from rest_framework import serializers

from .models import (Order, OrderItem)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields= '__all__'

class PlaceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields= ("full_name","address","city","phone","post_code")
        optional_fields= ("full_name","address","city","phone","post_code")

class ChangeOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields= ('delivery_status',)

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'