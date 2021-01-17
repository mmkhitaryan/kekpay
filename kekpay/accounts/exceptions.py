from rest_framework.exceptions import APIException

class InsufficientFundsError(APIException):
    status_code = 403
    default_detail = 'Insufficient funds'
    default_code = 'insufficient_funds'

class NoDestinationAccount(APIException):
    status_code = 404
    default_detail = 'No destination account found'
    default_code = 'no_destination_account'

class NoSourceAccount(APIException):
    status_code = 404
    default_detail = 'No source account found'
    default_code = 'no_source_account'

class CannotTransactYourself(APIException):
    status_code = 404
    default_detail = 'You can not transact to yourself'
    default_code = 'cannot_transact_yourself'

class TransferAmmountMustBeNaturalNumber(APIException):
    status_code = 400
    default_detail = 'Transfer amount must be more or not zero'
    default_code = 'transfer_amount_must_be_natural_number'

class YouCannotTransferFromOthersAccounts(APIException):
    status_code = 400
    default_detail = 'You can not transfer from others accounts'
    default_code = 'cannot_transfer_from_others_accounts'

class YouCannotTransactToDifferentCurrencyAccounts(APIException):
    status_code = 400
    default_detail = 'You can not transfer to different currency accounts'
    default_code = 'cannot_transfer_to_different_currency_account'
