from unittest.util import _MAX_LENGTH
from rest_framework import serializers

from .models import (BankAccount, Transaction)

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields= '__all__'


class BankAccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields= ('credential','account_no',)


class BankAccountCreateSerializer_(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields= ('credential',)


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

class AddMoneyRequestSerializer_(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('account_to', 'amount')


class SendMoneyRequestSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='S',  max_length = 1)
    class Meta:
        model = Transaction
        fields = ('id', 'account_from' , 'credential', 'account_to', 'amount', 'status','type')

class SendMoneyRequestSerializer_(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('account_from' , 'credential', 'account_to', 'amount')