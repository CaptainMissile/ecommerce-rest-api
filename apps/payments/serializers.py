from rest_framework import serializers

from .models import (Payment)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields= '__all__'

class MakePaymentSerializer(serializers.Serializer):
    account_from = serializers.IntegerField(required=False)
    order_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=7, decimal_places=2)
    credential = serializers.CharField()