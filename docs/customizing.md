# Customizing

While `drf-pyseto` provides complete defaults for obtaining and refreshing tokens, you might want to extend the tokens with custom claims or modify how users are authenticated.

## Adding Custom Claims

By default, the PASETO Payload contains standard reserved claims (`exp`, `iat`) and your configured claims (`user_id_claim`, `token_type_claim`).

If you wish to embed additional user data into the token (such as roles, permissions, or profile IDs), you can extend the token creation logic by overriding the authentication view or by directly utilizing the core token classes.

```python
from drf_pyseto.tokens import AccessToken, RefreshToken

def get_tokens_for_user(user):
    # Generates standard tokens
    refresh = RefreshToken.for_user(user)
    access = AccessToken.for_user(user)
    
    # Inject custom claims
    access["role"] = user.role
    access["email"] = user.email

    return {
        "refresh": refresh.encode(),
        "access": access.encode(),
    }
```

> **Warning:** Because `v4.local` uses symmetric encryption, clients cannot read the claims. If your frontend app needs to know the user's `role`, you should send it separately in the JSON response rather than relying on the frontend parsing the token.

## Customizing the Authentication Class

If you need to change how the bearer token is extracted from the `Authorization` header, or if you want to perform additional checks (such as verifying if a user is still active in the database), you can subclass `PASETOAuthentication`:

```python
from drf_pyseto.authentication import PASETOAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomPASETOAuthentication(PASETOAuthentication):
    def authenticate(self, request):
        auth_result = super().authenticate(request)
        if auth_result is None:
            return None
        
        user, token = auth_result
        
        # Add your custom business logic
        if not user.is_active:
            raise AuthenticationFailed("User account is disabled.")

        return (user, token)
```

Don't forget to update your `DEFAULT_AUTHENTICATION_CLASSES` in `settings.py` to point to your new `CustomPASETOAuthentication` class instead of the default.
