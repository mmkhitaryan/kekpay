from rest_framework.exceptions import APIException

class ChallengeInvalidAttempt(APIException):
    status_code = 403
    default_detail = 'Invalid challenge code'
    default_code = 'invalid_challenge'
