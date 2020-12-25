import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from kekpay.accounts.models import Account

class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=11, unique=True)
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE
    )

    USERNAME_FIELD = 'phone'
