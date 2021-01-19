import uuid
from decimal import Decimal

from django.db import models
from django.db import transaction
from django.utils import timezone

from .exceptions import InsufficientFundsError
from .currencies import currencies_choices, get_currency_by_code

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
        default=0,
    )
    created_at = models.DateTimeField(default=timezone.now)


class Account(models.Model):
    balance = models.DecimalField( # они сами квантазируют по decimal_places??
        max_digits=255,
        decimal_places=8,
        default=0,
    )
    _currency = models.CharField(
        max_length=3,
        choices=currencies_choices,
        default='USD',
    )

    @property
    def currency(self):
        return get_currency_by_code(self._currency)

    @currency.setter
    def currency(self, value):
        self._currency = value

    def clean(self):
        N_PLACES_DECIMAL = Decimal(10) ** self.currency.minimal_piece
        self.balance = self.balance.quantize(N_PLACES_DECIMAL)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Account, self).save(*args, **kwargs)
