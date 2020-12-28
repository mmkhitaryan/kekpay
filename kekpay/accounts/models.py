import uuid

from django.db import models
from django.db import transaction
from .exceptions import InsufficientFundsError
from django.utils import timezone
from django.conf import settings

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
        max_digits=12,
        decimal_places=2
    )
    created_at = models.DateTimeField(default=timezone.now)


class Account(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2, 
        default=0
    )
