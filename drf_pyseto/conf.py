from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Any, Optional

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


DEFAULTS = {
    "ACCESS_LIFETIME": 300,
    "REFRESH_LIFETIME": 86400,
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "TOKEN_TYPE_CLAIM": "typ",
    "AUTH_HEADER_TYPE": "Bearer",
    "ISSUER": None,
    "AUDIENCE": None,
}


@dataclass(frozen=True)
class PASETOSettings:
    key: bytes
    access_lifetime: int
    refresh_lifetime: int
    user_id_field: str
    user_id_claim: str
    token_type_claim: str
    auth_header_type: str
    issuer: Optional[str]
    audience: Optional[str]


def _b64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def _normalize_key(value: Any) -> bytes:
    if value is None:
        raise ImproperlyConfigured("DRF_PYSETO['KEY'] is required")
    if isinstance(value, bytes):
        key_bytes = value
    elif isinstance(value, str):
        try:
            decoded = _b64url_decode(value)
        except Exception:
            decoded = None

        if decoded and len(decoded) == 32:
            key_bytes = decoded
        else:
            key_bytes = value.encode("utf-8")
    else:
        raise ImproperlyConfigured("DRF_PYSETO['KEY'] must be bytes or str")

    if len(key_bytes) != 32:
        raise ImproperlyConfigured("DRF_PYSETO['KEY'] must be 32 bytes for v4.local")
    return key_bytes


def get_settings() -> PASETOSettings:
    raw = getattr(settings, "DRF_PYSETO", {})
    if raw is None:
        raw = {}

    key = _normalize_key(raw.get("KEY"))

    def _get_int(name: str) -> int:
        value = raw.get(name, DEFAULTS[name])
        if not isinstance(value, int) or value <= 0:
            raise ImproperlyConfigured(f"DRF_PYSETO['{name}'] must be a positive int")
        return value

    return PASETOSettings(
        key=key,
        access_lifetime=_get_int("ACCESS_LIFETIME"),
        refresh_lifetime=_get_int("REFRESH_LIFETIME"),
        user_id_field=raw.get("USER_ID_FIELD", DEFAULTS["USER_ID_FIELD"]),
        user_id_claim=raw.get("USER_ID_CLAIM", DEFAULTS["USER_ID_CLAIM"]),
        token_type_claim=raw.get("TOKEN_TYPE_CLAIM", DEFAULTS["TOKEN_TYPE_CLAIM"]),
        auth_header_type=raw.get("AUTH_HEADER_TYPE", DEFAULTS["AUTH_HEADER_TYPE"]),
        issuer=raw.get("ISSUER", DEFAULTS["ISSUER"]),
        audience=raw.get("AUDIENCE", DEFAULTS["AUDIENCE"]),
    )
