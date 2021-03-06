from django.db import models
from django.utils.translation import gettext_lazy as _

class BaseCurrency():
    pass

class DigitalCurrency(BaseCurrency):
    minimal_piece = 1000000

class RealCurrencyBase(BaseCurrency):
    pass

class RealCurrencyBaseHundred(RealCurrencyBase):
    minimal_piece = 100

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

currencies_list = {
    'USD': USD,
    'RUB': RUB,
    'KZT': KZT,
    'BTC': BTC,
    'LTC': LTC,
}

currencies_choices = [
    ('USD', 'United States dollar'),
    ('RUB', 'Russian Ruble'),
    ('KZT', 'Tenge'),
    ('BTC', 'Bitcoin'),
    ('LTC', 'Litecoin')
]

def get_currency_by_code(code):
    return currencies_list[code]
