from django.test import TestCase
from .models import Account
from .services import transfer_from_to
from .exceptions import InsufficientFundsError
import pytest

class TransactionsTestCase(TestCase):
    def setUp(self):
        self.firest_account = Account.objects.create(balance=1)
        self.second_account = Account.objects.create(balance=100)

    def test_transfer_from_first_to_second_good(self):
        a = transfer_from_to(self.second_account, self.firest_account, 100)
        a.balance == 0

        assert self.firest_account.balance == 101

    def test_transfer_from_second_to_first_good(self):
        a = transfer_from_to(self.firest_account, self.second_account, 1)
        a.balance == 0

        assert self.second_account.balance == 101

    def test_insufficient_funds(self):
        with pytest.raises(InsufficientFundsError) as excinfo:
            a = transfer_from_to(self.firest_account, self.second_account, 2)
            a.balance == 0
