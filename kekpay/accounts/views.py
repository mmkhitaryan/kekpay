from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.response import Response

from .services import transfer_from_to, get_own_transaction_history
from .serializers import DoTransactionSerializer, AccountSerializer
from .exceptions import YouCannotTransferFromOthersAccounts, NoSourceAccount

UserModel = get_user_model()

class TransactionView(ViewSet):
    def get(self, request, format=None):
        queryset = get_own_transaction_history(request.user)
        return Response(queryset)

    @action(
        methods=['post'],
        detail=False
    )
    def transfer_to(self, request):
        transfer_serializer = DoTransactionSerializer(data=request.data)
        transfer_serializer.is_valid(raise_exception=True)

        source_account = transfer_serializer.validated_data['source_account']
        destination_account = transfer_serializer.validated_data['destination_account']

        try:
            source_account_owner = UserModel.objects.get(accounts__in=[source_account])
        except UserModel.DoesNotExist:
            raise NoSourceAccount

        if source_account_owner!=request.user:
            raise YouCannotTransferFromOthersAccounts

        transfer_from_to(
            source_account,
            destination_account,
            transfer_serializer.validated_data['amount']
        )

        serializer = AccountSerializer(source_account)
        return Response(serializer.data)
