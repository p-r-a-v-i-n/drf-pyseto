from __future__ import annotations

from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ImproperlyConfigured
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .conf import get_settings
from .tokens import create_access_token, create_refresh_token, decode_token


class TokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        request = self.context.get("request")
        user = authenticate(request=request, username=attrs.get("username"), password=attrs.get("password"))
        if user is None:
            raise AuthenticationFailed("Invalid credentials")
        if not user.is_active:
            raise AuthenticationFailed("User inactive")

        return {
            "access": create_access_token(getattr(user, get_settings().user_id_field)),
            "refresh": create_refresh_token(getattr(user, get_settings().user_id_field)),
        }


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        settings = get_settings()
        token = attrs.get("refresh")
        try:
            payload = decode_token(token)
        except ImproperlyConfigured as exc:
            raise AuthenticationFailed(str(exc)) from exc
        except Exception as exc:
            raise AuthenticationFailed("Invalid refresh token") from exc

        if payload.get(settings.token_type_claim) != "refresh":
            raise AuthenticationFailed("Invalid token type")

        user_id = payload.get(settings.user_id_claim)
        if user_id is None:
            raise AuthenticationFailed("Missing user claim")

        user = _get_user(user_id, settings.user_id_field)
        if user is None or not user.is_active:
            raise AuthenticationFailed("User not found")

        return {"access": create_access_token(user_id)}


def _get_user(user_id, field: str):
    user_model = get_user_model()
    try:
        return user_model.objects.get(**{field: user_id})
    except user_model.DoesNotExist:
        return None
