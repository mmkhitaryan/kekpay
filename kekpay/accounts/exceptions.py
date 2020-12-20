from rest_framework.exceptions import APIException

class InsufficientFundsError(APIException):
    status_code = 403
    default_detail = 'Insufficient funds'
    default_code = 'insufficient_funds'
