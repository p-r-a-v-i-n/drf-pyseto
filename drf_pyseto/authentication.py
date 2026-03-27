from __future__ import annotations

from typing import Optional, Tuple

from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from .conf import get_settings
from .tokens import decode_token


class PASETOAuthentication(BaseAuthentication):
    def authenticate(self, request) -> Optional[Tuple[object, dict]]:
        settings = get_settings()
        auth = get_authorization_header(request).split()
        if not auth:
            return None

        if auth[0].decode("utf-8").lower() != settings.auth_header_type.lower():
            return None

        if len(auth) == 1:
            raise AuthenticationFailed("Invalid Authorization header. No credentials provided.")
        if len(auth) > 2:
            raise AuthenticationFailed("Invalid Authorization header. Token string should not contain spaces.")

        token = auth[1].decode("utf-8")
        try:
            payload = decode_token(token)
        except ImproperlyConfigured as exc:
            raise AuthenticationFailed(str(exc)) from exc
        except Exception as exc:
            raise AuthenticationFailed("Invalid token") from exc

        token_type = payload.get(settings.token_type_claim)
        if token_type != "access":
            raise AuthenticationFailed("Invalid token type")

        user_id = payload.get(settings.user_id_claim)
        if user_id is None:
            raise AuthenticationFailed("Missing user claim")

        user = _get_user(user_id, settings.user_id_field)
        if user is None:
            raise AuthenticationFailed("User not found")
        if not user.is_active:
            raise AuthenticationFailed("User inactive")

        return (user, payload)


def _get_user(user_id, field: str):
    user_model = get_user_model()
    try:
        return user_model.objects.get(**{field: user_id})
    except user_model.DoesNotExist:
        return None
