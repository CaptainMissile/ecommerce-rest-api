from unittest.util import _MAX_LENGTH
from rest_framework import serializers

from .models import (BankAccount, Transaction)

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields= '__all__'


class BankAccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields= ('credential',)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields= '__all__'


class AddMoneyRequestSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='I', max_length = 1)

    class Meta:
        model = Transaction
        fields = ('id', 'account_to', 'amount', 'status','type')


class SendMoneyRequestSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='S',  max_length = 1)
    class Meta:
        model = Transaction
        fields = ('id', 'account_from' , 'credential', 'account_to', 'amount', 'status','type')