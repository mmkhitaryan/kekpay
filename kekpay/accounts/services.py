from django.db import models
from django.db import transaction
from django.db.models import Q

from django.contrib.auth import get_user_model

from .models import Account, TransactionHistory
from .exceptions import InsufficientFundsError

UserModel = get_user_model()

def get_own_transaction_history(me_user):
    my_account = me_user.account

    own_transactions = TransactionHistory.objects.filter(
        Q(from_account=my_account) |
        Q(to_account=my_account)
    )
    return own_transactions

def transfer_balance_from_user_to_user(from_user, to_user, amount):
    from_account = from_user.account
    to_account = to_user.account

    return transfer_from_to(to_account, from_account, amount)

def transfer_from_to(source_account, destination_account, amount):
    with transaction.atomic():
        Account.objects.select_for_update().filter(
            id__in=(
                source_account.id,
                destination_account.id
            )
        )

        if source_account.balance < amount:
            raise InsufficientFundsError

        source_account.balance-=amount
        destination_account.balance+=amount

        destination_account.save()
        source_account.save()
        return source_account
