from django.test import TestCase
from .models import Account

class AnimalTestCase(TestCase):
    def setUp(self):
        self.firest_account = Account.objects.create(balance=1)
        self.second_account = Account.objects.create(balance=100)

    def test_transfer_from_first_to_second_good(self):
        a = Account.transfer(self.second_account, self.firest_account)
        a.balance == 0

        assert self.firest_account.balance == 101

    def test_transfer_from_second_to_first_good(self):
        a = Account.transfer(self.firest_account, self.second_account)
        a.balance == 0

        assert self.second_account.balance == 101

    def test_insufficient_funds(self):
        pass