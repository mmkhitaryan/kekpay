import freezegun

from django.urls import reverse
from nose.tools import ok_, eq_
from rest_framework.test import APITestCase
from rest_framework import status
from .factories import UserFactory

dummy_challenge_code = 'ABC2'
def dummy_return(*args):
    return dummy_challenge_code

class TestChallenge(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.obtain_token_url = reverse('obtain-token')
        self.attempt_challenge_url = reverse('attempt-challenge')

    def test_get_request_returns_a_given_user(self):
        from kekpay.users.auth import JwtManager
        import kekpay.users.auth

        kekpay.users.auth.get_challenge_code = dummy_return
        
        response = self.client.post(self.obtain_token_url, {'phone': '77082333945'})

        token = response.json()['challenge_jwt']
        decoded = JwtManager.decode(token)
        assert decoded['phone'] == '77082333945'

        eq_(response.status_code, status.HTTP_200_OK)
        return token

    def test_success_attempt(self):
        data = self.test_get_request_returns_a_given_user()
        response = self.client.post(self.attempt_challenge_url, 
            {
                'challenge_jwt': data,
                'challenge_code': dummy_challenge_code
            }
        )
