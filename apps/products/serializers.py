from rest_framework import serializers

from .models import (Category, ProductInventory)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields= '__all__'

class ProductInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInventory
        fields = '__all__'

class ProductInventoryUpdateSerializer(serializers.Serializer):
    store = serializers.IntegerField(required=False)
    category= serializers.IntegerField(required=False)

    name = serializers.CharField(required=False)
    desc = serializers.CharField(required=False)
    price = serializers.DecimalField(required=False, max_digits=7, decimal_places=2)
    units = serializers.IntegerField(required=False)
    units_sold = serializers.IntegerField(required=False)

    is_active = serializers.IntegerField(required=False)