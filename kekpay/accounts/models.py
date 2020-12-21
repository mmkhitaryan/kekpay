import uuid

from django.db import models
from django.db import transaction
from .exceptions import InsufficientFundsError

class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance = models.DecimalField(max_digits=8, decimal_places=2)

    @classmethod
    def transfer(cls, source_account, destination_account, amount):
        with transaction.atomic():
            cls.objects.select_for_update().filter(
                id__in=(
                    source_account.id,
                    destination_account.id
                )
            )

            if source_account.balance < amount:
                raise InsufficientFundsError

            source_account.balance-=amount
            destination_account.balance+=amount

            # TODO: take balance from source_account, give balance to destination_account
            destination_account.save()
            source_account.save()
            return source_account
