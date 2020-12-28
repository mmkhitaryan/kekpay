from django.db import models
from django.db import transaction
from django.db.models import Q

from django.contrib.auth import get_user_model

from .models import Account, TransactionHistory
from .exceptions import InsufficientFundsError, CannotTransactYourself, TransferAmmountMustBeNaturalNumber

UserModel = get_user_model()

def get_own_transaction_history(me_user):
    my_accounts = me_user.accounts.all()

    # TODO: mark transactions as in and out for output
    own_transactions = TransactionHistory.objects.filter(
        Q(from_account__in=my_accounts) |
        Q(to_account__in=my_accounts)
    )
    return own_transactions

# TODO: write transction history
def transfer_from_to(source_account, destination_account, amount):
    if source_account.pk == destination_account.pk:
        raise CannotTransactYourself

    if amount<=0:
        raise TransferAmmountMustBeNaturalNumber

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
