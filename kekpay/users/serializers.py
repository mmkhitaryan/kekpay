from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User
from .auth import OneTimeTokenAuthManager
from rest_framework_simplejwt.tokens import RefreshToken

class CreateChallengeSerializer(serializers.Serializer):
    phone = serializers.CharField(
        label=_("Phone number"),
        write_only=True,
        max_length=11
    )
    challenge_jwt = serializers.CharField(
        read_only=True
    )

    def validate(self, attrs):
        new_attrs = {}
        phone = attrs.get('phone')

        code = OneTimeTokenAuthManager.get_jwt_challenge_for_phone(phone)
        new_attrs['challenge_jwt']=code

        return new_attrs

class AttemntChallengeSerializer(serializers.Serializer):
    challenge_jwt = serializers.CharField(
        write_only=True
    )
    challenge_code = serializers.CharField(
        label=_("SMS code"),
        write_only=True,
        max_length=OneTimeTokenAuthManager.code_size
    )

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        new_attrs = {}

        challenge_jwt = attrs.get('challenge_jwt')
        challenge_code = attrs.get('challenge_code')

        self.user = OneTimeTokenAuthManager.attemt_jwt_challenge_solve(
            challenge_jwt, 
            challenge_code
        )

        refresh = self.get_token(self.user)

        data = {}

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data
