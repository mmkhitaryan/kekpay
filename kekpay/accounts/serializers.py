from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Account

class DoTransactionSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    transfer_destination = serializers.UUIDField()
    source_account = serializers.UUIDField()

    def validate(self, attrs):
        source_account = get_object_or_404(Account, id=attrs['source_account'])
        attrs['source_account'] = source_account

        destination_account = get_object_or_404(Account, id=attrs['transfer_destination'])
        attrs['destination_account'] = destination_account
        return attrs

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'balance']
