import datetime
import jwt
import random
import string
import base64

from django.utils.crypto import constant_time_compare, salted_hmac, get_random_string
from django.conf import settings

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

        return JwtManager.encode(
            {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=cls.expr_secods),
                'phone': phone,
                'challenge_hmac': challenge_hmac
            }
        )
