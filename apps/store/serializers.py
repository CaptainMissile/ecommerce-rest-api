from rest_framework import serializers

from .models import Store

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

    def create(self, validated_data):
        return Store.objects.create(**validated_data)