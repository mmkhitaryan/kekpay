import freezegun

from django.urls import reverse
from nose.tools import eq_
from rest_framework.test import APITestCase
from rest_framework import status
from .factories import UserFactory
from kekpay.users.auth import OneTimeTokenAuthManager

dummy_challenge_code = 'ABC2'
def dummy_return(*args):
    return dummy_challenge_code

def get_outdated_jwt():
    # Freezing time
    with freezegun.freeze_time("2012-01-14"):
        return OneTimeTokenAuthManager.get_jwt_challenge_for_phone('77082113945')[0].decode()

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
        ).json()

        assert response['refresh']
        assert response['access']
    
    def test_too_late(self):
        response = self.client.post(self.attempt_challenge_url, 
            {
                'challenge_jwt': get_outdated_jwt(),
                'challenge_code': dummy_challenge_code
            }
        ).json()

        assert response['detail'] == 'Too late, retry with a new SMS code'

    def test_invalid_data(self):
        response = self.client.post(self.attempt_challenge_url, 
            {
                'challenge_jwt': 'aasdfasdf.asdfasdf.2asdfasdfaf',
                'challenge_code': dummy_challenge_code
            }
        ).json()

        assert response['detail'] == 'Invalid token'

    def test_invalid_code(self):
        data = self.test_get_request_returns_a_given_user()
        response = self.client.post(self.attempt_challenge_url, 
            {
                'challenge_jwt': data,
                'challenge_code': 'ad13'
            }
        ).json()

        assert response['detail'] == 'Invalid challenge code'
