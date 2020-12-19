import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser

from rest_framework.authtoken.models import Token


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=11, unique=True)

    USERNAME_FIELD = 'phone'
