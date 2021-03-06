import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from kekpay.accounts.models import Account

class User(AbstractBaseUser):
    phone = models.CharField(
        max_length=11,
        unique=True,
        null=False
    )
    accounts = models.ManyToManyField(
        Account, related_name='owners'
    )

    USERNAME_FIELD = 'phone'
