from __future__ import annotations

import json
import time
from typing import Any, Dict

import pyseto
from django.core.exceptions import ImproperlyConfigured

from .conf import get_settings

ALLOWED_TYPES = {"access", "refresh"}
LEEWAY_SECONDS = 30


def _now() -> int:
    return int(time.time())


def _get_paseto_key(key_bytes: bytes):
    if hasattr(pyseto, "Key"):
        return pyseto.Key.new(version=4, purpose="local", key=key_bytes)
    return key_bytes


def _encode_paseto(key_bytes: bytes, payload: Dict[str, Any]) -> str:
    key = _get_paseto_key(key_bytes)
    try:
        token = pyseto.encode(key, payload, serializer=json)
    except TypeError:
        # Older pyseto may not accept serializer= for dict payloads
        token = pyseto.encode(key, json.dumps(payload))
    if isinstance(token, bytes):
        return token.decode("utf-8")
    return str(token)


def _decode_paseto(key_bytes: bytes, token: str) -> Dict[str, Any]:
    key = _get_paseto_key(key_bytes)
    try:
        decoded = pyseto.decode(key, token)
    except TypeError:
        decoded = pyseto.decode(key, token)

    payload = decoded
    if hasattr(decoded, "payload"):
        payload = decoded.payload
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8")
    if isinstance(payload, str):
        payload = json.loads(payload)

    if not isinstance(payload, dict):
        raise ImproperlyConfigured("Decoded PASETO payload must be a JSON object")
    return payload


def _validate_payload(payload: Dict[str, Any]) -> None:
    settings = get_settings()
    token_type = payload.get(settings.token_type_claim)
    if token_type not in ALLOWED_TYPES:
        raise ImproperlyConfigured("Invalid token type claim")

    exp = payload.get("exp")
    if not isinstance(exp, int):
        raise ImproperlyConfigured("Token exp must be an int timestamp")
    if exp < (_now() - LEEWAY_SECONDS):
        raise ImproperlyConfigured("Token has expired")


def create_token(user_id: Any, token_type: str, lifetime_seconds: int) -> str:
    settings = get_settings()
    if token_type not in ALLOWED_TYPES:
        raise ImproperlyConfigured("Token type must be 'access' or 'refresh'")

    issued_at = _now()
    payload = {
        settings.user_id_claim: user_id,
        "iat": issued_at,
        "exp": issued_at + lifetime_seconds,
        settings.token_type_claim: token_type,
    }
    if settings.issuer:
        payload["iss"] = settings.issuer
    if settings.audience:
        payload["aud"] = settings.audience

    return _encode_paseto(settings.key, payload)


def create_access_token(user_id: Any) -> str:
    settings = get_settings()
    return create_token(user_id, "access", settings.access_lifetime)


def create_refresh_token(user_id: Any) -> str:
    settings = get_settings()
    return create_token(user_id, "refresh", settings.refresh_lifetime)


def decode_token(token: str) -> Dict[str, Any]:
    settings = get_settings()
    payload = _decode_paseto(settings.key, token)
    _validate_payload(payload)

    if settings.issuer and payload.get("iss") != settings.issuer:
        raise ImproperlyConfigured("Invalid token issuer")
    if settings.audience and payload.get("aud") != settings.audience:
        raise ImproperlyConfigured("Invalid token audience")

    return payload
