from django.test import TestCase
from rest_framework.test import APIClient

from rest_framework.test import force_authenticate
from django.contrib.auth import get_user_model

from kekpay.accounts.models import Account

UserModel = get_user_model()


class E2ETransactionsApiTestCase(TestCase):
    def setUp(self):
        self.first_user_account = Account.objects.create(balance=1)
        self.first_user = UserModel.objects.create(phone='77777334')
        self.first_user.accounts.add(self.first_user_account)
        self.first_user.save()

        self.second_user_account = Account.objects.create(balance=3)
        self.second_user = UserModel.objects.create(phone='77777324')
        self.second_user.accounts.add(self.second_user_account)
        self.second_user.save()

        client = APIClient()
        client.force_authenticate(user=self.first_user)
        self.client = client

    def test_transaction_from_first_to_second_successful(self):
        t = self.client.post('/api/transactions/transfer_to/',
            {
                'amount': '0.5',
                'transfer_destination': self.second_user_account.pk,
                'source_account': self.first_user_account.pk
            },
            format='json'
        )
        t = t.json()

        self.first_user_account.refresh_from_db()
        self.second_user_account.refresh_from_db()

        assert self.first_user_account.balance == 0.5
        assert self.second_user_account.balance == 3.5

    def test_transaction_from_first_to_second_invalid_amount(self):
        t = self.client.post('/api/transactions/transfer_to/',
            {
                'amount': '-2',
                'transfer_destination': self.second_user_account.pk,
                'source_account': self.first_user_account.pk
            },
            format='json'
        )
        t = t.json()
        self.first_user_account.refresh_from_db()
        assert self.first_user_account.balance == 1
        
        assert t['detail'] == 'Transfer amount must be more or not zero'

    def test_transaction_from_first_to_second_insufficent_funds(self):
        t = self.client.post('/api/transactions/transfer_to/',
            {
                'amount': '2222',
                'transfer_destination': self.second_user_account.pk,
                'source_account': self.first_user_account.pk
            },
            format='json'
        )
        t = t.json()
        self.first_user_account.refresh_from_db()
        assert self.first_user_account.balance == 1
        
        assert t['detail'] == 'Insufficient funds'

    def test_transaction_from_others_account(self):
        t = self.client.post('/api/transactions/transfer_to/',
            {
                'amount': '2',
                'transfer_destination': self.first_user_account.pk,
                'source_account': self.second_user_account.pk
            },
            format='json'
        )
        t = t.json()
        self.first_user_account.refresh_from_db()
        assert self.first_user_account.balance == 1
        assert t['detail'] == 'You can not transfer from others accounts'

    def test_transaction_from_not_found_destination(self):
        t = self.client.post('/api/transactions/transfer_to/',
            {
                'amount': '2222',
                'transfer_destination': '912221f8-25d9-45fe-b120-0b37c9a1720c',
                'source_account': self.second_user_account.pk
            },
            format='json'
        )
        t = t.json()
        assert t['detail'] == 'No destination account found'

    def test_transaction_from_not_found_source(self):
        t = self.client.post('/api/transactions/transfer_to/',
            {
                'amount': '2222',
                'transfer_destination': self.first_user_account.pk,
                'source_account': '912221f8-25d9-45fe-b120-0b37c9a1720c'
            },
            format='json'
        )
        t = t.json()
        self.first_user_account.refresh_from_db()
        assert self.first_user_account.balance == 1
        assert t['detail'] == 'No source account found'

    def test_transaction_history(self):
        self.test_transaction_from_first_to_second_successful()
        response = self.client.get('/api/transactions/').json()
        assert response[0]['way'] == 'out'

        self.test_transaction_from_first_to_second_successful()
        self.client.force_authenticate(user=self.second_user)
        response = self.client.get('/api/transactions/').json()
        assert response[0]['way'] == 'in'

    # TODO: Add test for multiple transaction history enteties
