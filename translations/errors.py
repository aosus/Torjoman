from ninja_extra import status
from ninja_extra.exceptions import APIException


class PermissionError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "not_allowed"


class LimitError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "limit_error"
