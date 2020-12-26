from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from .services import transfer_balance_from_user_to_user, get_own_transaction_history

class TransactionView(APIView):
    def get(self, request, format=None):
        queryset = get_own_transaction_history(request.user)
        return Response(queryset)

    @action(detail=True, methods=['post'])
    def transfer_to(self, request, pk):

        transfer_balance_from_user_to_user()