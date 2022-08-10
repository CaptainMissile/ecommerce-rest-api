from rest_framework import serializers

from .models import Store


class StoreSerializer(serializers.Serializer):
    class Meta:
        model = Store
        fields = '__all__'