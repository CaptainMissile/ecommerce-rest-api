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