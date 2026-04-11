# Getting Started

## Requirements

- Python >= 3.10
- Django >= 4.2
- Django REST Framework >= 3.16
- [pyseto](https://github.com/dajiaji/pyseto) >= 1.7

## Installation

Install the package via pip:

```bash
pip install drf-pyseto
```

## Basic Configuration

### 1. Update Django Settings

Add the necessary configuration for `drf-pyseto` in your `settings.py`. At a minimum, you must provide a 32-byte secret key:

```python
import secrets

DRF_PYSETO = {
    # Generate this one time using secrets.token_hex(16) or equivalent
    "KEY": "a-secure-32-byte-secret-key-strr", 
    "ACCESS_LIFETIME": 300,        # 5 minutes
    "REFRESH_LIFETIME": 86400,     # 1 day
}
```

### 2. Configure DRF Authentication

Set `drf_pyseto` as your authentication class in `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'drf_pyseto.authentication.PASETOAuthentication',
    )
}
```

If you only want to protect specific views, you can set it directly on your API views instead of modifying the global settings:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_pyseto.authentication import PASETOAuthentication

class ProtectedView(APIView):
    authentication_classes = [PASETOAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Hello, {request.user.username}!"})
```

### 3. Setup Routing

Include the built-in views in your project's `urls.py` in order to obtain and refresh tokens:

```python
from django.urls import path, include

urlpatterns = [
    # Your API URLs here...
    path("api/auth/", include("drf_pyseto.urls")),
]
```

## Next Steps

Now that your project is configured, check out [API Endpoints](endpoints.md) to learn how to obtain tokens, or refer to the [Settings](settings.md) for more customization options.
