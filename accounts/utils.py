import jwt
from datetime import datetime, timedelta
from django.conf import settings
from ninja.security import HttpBearer
from django.contrib.auth.models import User
from ninja.errors import ValidationError, AuthenticationError

JWT_SIGNING_KEY = getattr(settings, "JWT_SIGNING_KEY")
JWT_ACCESS_EXPIRY = getattr(settings, "JWT_ACCESS_EXPIRY")
JWT_REFRESH_EXPIRY = getattr(settings, "JWT_REFRESH_EXPIRY")
ACCESS_EXPIRY_PERIOD = timedelta(hours=JWT_ACCESS_EXPIRY)
REFRESH_EXPIRY_PERIOD = timedelta(hours=JWT_REFRESH_EXPIRY)


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        payload = _get_payload(token, "access")
        user_id: int = payload.get("id")
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise AuthenticationError
        return user


def _get_payload(token: str, type: str) -> dict[str, str]:
    try:
        payload = jwt.decode(token, JWT_SIGNING_KEY, algorithms=["HS256"])
    except jwt.PyJWTError:
        raise AuthenticationError
    if payload["type"] != type:
        raise ValidationError("invalid_token")
    diff = datetime.utcnow() - datetime.fromtimestamp(payload.get("expire_at", 0))
    if diff >= ACCESS_EXPIRY_PERIOD:
        raise AuthenticationError
    return payload


def create_token(user_id):
    access = jwt.encode(
        {
            "id": user_id,
            "type": "access",
            "expire_at": (datetime.utcnow() + ACCESS_EXPIRY_PERIOD).timestamp(),
        },
        JWT_SIGNING_KEY,
    )

    refresh = jwt.encode(
        {
            "id": user_id,
            "type": "refresh",
            "expire_at": (datetime.utcnow() + REFRESH_EXPIRY_PERIOD).timestamp(),
        },
        JWT_SIGNING_KEY,
    )
    return {"access": access, "refresh": refresh}


def refresh_access(refresh_token):
    payload = _get_payload(refresh_token, "refresh")
    user_id: int = payload.get("id")
    try:
        User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise AuthenticationError

    return create_token(user_id)
