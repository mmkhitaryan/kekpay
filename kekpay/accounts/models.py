import uuid

from django.db import models
from django.db import transaction
from django.utils import timezone
from django.conf import settings

from .exceptions import InsufficientFundsError
from .currencies import CurrenciesList

UserModel = settings.AUTH_USER_MODEL

class TransactionHistory(models.Model):
    from_account = models.ForeignKey(
        'Account',
        on_delete=models.CASCADE,
        related_name='from_account'
    )
    to_account = models.ForeignKey(
        'Account',
        on_delete=models.CASCADE,
        related_name='to_account'
    )

    amount = models.DecimalField(
        max_digits=255,
        decimal_places=6,
    )
    created_at = models.DateTimeField(default=timezone.now)



class Account(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    balance = models.DecimalField(
        max_digits=255,
        decimal_places=6,
        default=0,
    )
