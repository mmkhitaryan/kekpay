from django.db import models

class BaseCurrency():
    pass

class DigitalCurrency(BaseCurrency):
    number_to_basic = 0

class RealCurrencyBase(BaseCurrency):
    pass

class RealCurrencyBaseHundred(RealCurrencyBase):
    number_to_basic = 2

class USD(RealCurrencyBaseHundred):
    pass

class RUB(RealCurrencyBaseHundred):
    pass

class KZT(RealCurrencyBaseHundred):
    pass

class BTC(DigitalCurrency):
    pass

class LTC(DigitalCurrency):
    pass

class CurrenciesList(models.TextChoices):
    USD = USD, 'USD'

