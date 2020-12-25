from rest_framework.exceptions import APIException

class ChallengeInvalidAttempt(APIException):
    status_code = 401
    default_detail = 'Invalid challenge code'
    default_code = 'invalid_challenge'

class ChallengeInvalidData(APIException):
    status_code = 400
    default_detail = 'Invalid token'
    default_code = 'invalid_token'

class ChallengeExpired(APIException):
    status_code = 401
    default_detail = 'Too late, retry with a new SMS code'
    default_code = 'too_late'
