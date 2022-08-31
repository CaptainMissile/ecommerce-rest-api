from rest_framework import serializers

from .models import Store

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

class StoreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('name', 'location', 'description')


class StoreUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'
        read_only_fields = ('id','owner',)
        optional_fields = [ 'name', 'location', 'description']