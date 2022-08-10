from rest_framework import serializers

from .models import (BankAccount, Transaction)

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields= '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'