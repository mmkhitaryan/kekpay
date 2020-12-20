import uuid

from django.db import models
from django.db import transaction

class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance = models.DecimalField(max_digits=8, decimal_places=2)

    @classmethod
    def transfer(cls, source_account, destination_account):
        with transaction.atomic():
            cls.objects.select_for_update().filter(
                id__in=(
                    source_account.id,
                    destination_account.id
                )
            )

            # TODO: take from self, give to to
            destination_account.save()
            source_account.save()
            return source_account
