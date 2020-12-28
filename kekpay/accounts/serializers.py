from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Account, TransactionHistory
from .exceptions import NoSourceAccount, NoDestinationAccount

class DoTransactionSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    transfer_destination = serializers.UUIDField()
    source_account = serializers.UUIDField()

    def validate(self, attrs):
        try:
            source_account = Account.objects.get(id=attrs['source_account'])
            attrs['source_account'] = source_account
        except Account.DoesNotExist:
            raise NoSourceAccount

        try:
            destination_account = Account.objects.get(id=attrs['transfer_destination'])
            attrs['destination_account'] = destination_account
        except Account.DoesNotExist:
            raise NoDestinationAccount
        return attrs

class TransactionsHistorySeriazlier(serializers.ModelSerializer):
    way = serializers.CharField()

    class Meta:
        model = TransactionHistory
        fields = ['id', 'amount', 'created_at', 'way']

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'balance']
