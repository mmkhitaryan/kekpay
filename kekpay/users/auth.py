import datetime
import random
import string
import base64
import hashlib

import jwt

from django.utils.crypto import constant_time_compare, salted_hmac, get_random_string
from django.conf import settings

from .exceptions import ChallengeInvalidAttempt, ChallengeExpired, ChallengeInvalidData

def get_challenge_code(N):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))

def get_hmac_for_challenge_code(code):
    return base64.b64encode(
        salted_hmac('OneTimeTokenAuthManager', code).digest()
    ).decode()

class JwtManager():
    @classmethod
    def encode(cls, obj):
        return jwt.encode(obj, settings.SECRET_KEY, algorithm='HS256')

    @classmethod
    def decode(cls, obj):
        return jwt.decode(obj, settings.SECRET_KEY, algorithm='HS256')

class OneTimeTokenAuthManager():
    expr_secods = 60*30 # 15 minutes lifetime
    code_size = 4

    @classmethod
    def get_jwt_challenge_for_phone(cls, phone):
        challenge_code = get_challenge_code(cls.code_size)
        challenge_hmac = get_hmac_for_challenge_code(challenge_code)
        print(challenge_code)
        return JwtManager.encode(
            {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=cls.expr_secods),
                'phone': phone,
                'challenge_hmac': challenge_hmac
            }
        )

    @classmethod
    def attemt_jwt_challenge_solve(cls, jwt, attemt_code):
        try:
            decoded_key = JwtManager.decode(jwt)
        except jwt.exceptions.ExpiredSignatureError:
            raise ChallengeExpired
        except jwt.exceptions.DecodeError:
            raise ChallengeInvalidData

        if decoded_key['challenge_hmac'] != get_hmac_for_challenge_code(attemt_code):
            raise ChallengeInvalidAttempt

        return jwt
