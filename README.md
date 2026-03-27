# drf-pyseto

Simple PASETO (v4.local) authentication for Django REST Framework using `pyseto`.

Targeted for Django 4.2–6.x and Python 3.10–3.14.

## Install

```bash
pip install drf-pyseto
```

## Dev Install

```bash
pip install -e ".[test]"
```

## Settings

```python
DRF_PYSETO = {
    "KEY": "<32-byte key or base64url>",
    "ACCESS_LIFETIME": 300,  # seconds
    "REFRESH_LIFETIME": 86400,  # seconds
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "TOKEN_TYPE_CLAIM": "typ",
    "AUTH_HEADER_TYPE": "Bearer",
    # Optional:
    # "ISSUER": "your-service",
    # "AUDIENCE": "your-clients",
}
```

## URLs

```python
from django.urls import path, include

urlpatterns = [
    path("api/auth/", include("drf_pyseto.urls")),
]
```

## DRF Authentication

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "drf_pyseto.authentication.PASETOAuthentication",
    ]
}
```

## Endpoints

- `POST /token/` with `username` and `password`
- `POST /token/refresh/` with `refresh`

## Tests

```bash
pytest
```
