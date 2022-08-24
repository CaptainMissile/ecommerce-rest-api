from rest_framework import serializers

from .models import (Order, OrderItem)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields= '__all__'

class ChangeOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields= ('delivery_status',)

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'