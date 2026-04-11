# drf-pyseto

[![PyPI version](https://img.shields.io/pypi/v/drf-pyseto.svg)](https://pypi.org/project/drf-pyseto/)
[![Python versions](https://img.shields.io/pypi/pyversions/drf-pyseto.svg)](https://pypi.org/project/drf-pyseto/)
[![Django versions](https://img.shields.io/pypi/djversions/drf-pyseto.svg)](https://pypi.org/project/drf-pyseto/)
[![License](https://img.shields.io/github/license/p-r-a-v-i-n/drf-pyseto.svg)](https://github.com/p-r-a-v-i-n/drf-pyseto/blob/main/LICENSE)

A simple, secure, and modern [PASETO (Platform-Agnostic Security Tokens)](https://paseto.io/) authentication backend for Django REST Framework (DRF), powered by [`pyseto`](https://github.com/dajiaji/pyseto).

`drf-pyseto` utilizes the **v4.local** (symmetric encryption) PASETO specification, providing a more secure alternative to JWTs by preventing cryptographic agility attacks and minimizing misconfigurations.

## 🌟 Features

- **Secure by Default:** Implements PASETO `v4.local` ensuring robust, symmetric encryption for your tokens.
- **Seamless Integration:** Built specifically for Django REST Framework. Drop-in replacement for traditional token or JWT authentication.
- **Configurable Lifetimes:** Easily manage separate lifetimes for access and refresh tokens.
- **Modern Python & Django Support:** Compatible with Python 3.10–3.14 and Django 4.2–6.0.

## 📦 Requirements

- Python >= 3.10
- Django >= 4.2
- Django REST Framework >= 3.16
- [pyseto](https://github.com/dajiaji/pyseto) >= 1.7

## 🚀 Installation

Install the package via pip:

```bash
pip install drf-pyseto
```

## ⚙️ Configuration

### 1. Update Django Settings

Add the necessary configuration for `drf-pyseto` in your `settings.py`:

```python
DRF_PYSETO = {
    # REQUIRED: A 32-byte secret key (can be plain 32-bytes or base64url encoded)
    "KEY": "<your-32-byte-secret-key-or-base64url>", 
    
    # Optional settings (defaults shown)
    "ACCESS_LIFETIME": 300,        # Access token lifetime in seconds (default: 5 minutes)
    "REFRESH_LIFETIME": 86400,     # Refresh token lifetime in seconds (default: 1 day)
    "USER_ID_FIELD": "id",         # User model field used as the subject
    "USER_ID_CLAIM": "user_id",    # Claim key for the user identifier
    "TOKEN_TYPE_CLAIM": "typ",     # Claim key for the token type
    "AUTH_HEADER_TYPE": "Bearer",  # Allowed Authorization header type

    # Additional standard PASETO claims (optional)
    # "ISSUER": "your-service",
    # "AUDIENCE": "your-clients",
}
```

### 2. Configure DRF Authentication

Set `drf_pyseto` as your authentication class in `settings.py`:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "drf_pyseto.authentication.PASETOAuthentication",
    )
}
```

### 3. Setup Routing

Include the token endpoints in your project's `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    # ...
    path("api/auth/", include("drf_pyseto.urls")),
    # ...
]
```

## 📡 Endpoints

Once configured, the following endpoints will be available to manage your tokens (assuming you included the URLs under `api/auth/`):

- **Obtain Tokens:** `POST /api/auth/token/`
  - *Payload:* `{"username": "your_username", "password": "your_password"}`
  - *Returns format:* `{"access": "v4.local....", "refresh": "v4.local...."}`

- **Refresh Access Token:** `POST /api/auth/token/refresh/`
  - *Payload:* `{"refresh": "v4.local...."}`
  - *Returns format:* `{"access": "v4.local...."}`

## 🛠️ Development & Testing

To set up the project for development and run the test suite:

```bash
# Clone the repository
git clone https://github.com/p-r-a-v-i-n/drf-pyseto.git
cd drf-pyseto

# Install locally with testing dependencies
pip install -e ".[test]"

# Run tests
pytest
```

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
