from django.db import models
from django.db import transaction
from .models import Account
from .exceptions import InsufficientFundsError

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
