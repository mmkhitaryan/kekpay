from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import User
from .auth import OneTimeTokenAuthManager


class CreateChallengeSerializer(serializers.Serializer):
    phone = serializers.CharField(
        label=_("Phone number"),
        write_only=True,
        max_length=11
    )
    challenge_jwt = serializers.JSONField(
        read_only=True
    )

    def validate(self, attrs):
        new_attrs = {}
        phone = attrs.get('username')
        new_attrs['challenge_jwt']='123'

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user

        return new_attrs