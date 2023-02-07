from ninja_extra import status
from ninja_extra.exceptions import APIException


class AlreadyExistError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "already_exists"


class IncorrectPasswordError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "incorrect_password"


class IncorrectResetCodeError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "incorrect_reset_code"
