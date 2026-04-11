# Settings

All configuration for `drf-pyseto` is managed through a single dictionary in your `settings.py` named `DRF_PYSETO`.

```python
DRF_PYSETO = {
    "KEY": "my-secure-32-byte-secret-key-strr",
    "ACCESS_LIFETIME": 300,
    "REFRESH_LIFETIME": 86400,
    # ... other settings
}
```

## Core Settings

### `KEY`
**Required.** Must be a 32-byte string (or a base64url encoded representation of a 32-byte key).
This key securely encrypts and decrypts the PASETO Payload. Because `v4.local` uses symmetric encryption, **you must never expose this key**. If this key is lost, all active tokens immediately become invalid.

### `ACCESS_LIFETIME`
**Default:** `300` (5 minutes)
The lifetime of the access token in seconds. Access tokens should generally be kept short-lived.

### `REFRESH_LIFETIME`
**Default:** `86400` (1 day)
The lifetime of the refresh token in seconds. This allows a user to stay authenticated over longer periods without needing to continually input their credentials.

## User Mapping

### `USER_ID_FIELD`
**Default:** `"id"`
The field on your custom Django `User` model that serves as a unique identifier. This field's value is what gets embedded into PASETO tokens.

### `USER_ID_CLAIM`
**Default:** `"user_id"`
The claim key inside the PASETO payload containing the User ID.

## Token Identifiers

### `TOKEN_TYPE_CLAIM`
**Default:** `"typ"`
The claim key inside the PASETO payload used to differentiate between `"access"` and `"refresh"` tokens. This prevents attackers from submitting a valid refresh token directly to an endpoint that expects an access token.

### `AUTH_HEADER_TYPE`
**Default:** `"Bearer"`
The string prefix expected in the `Authorization` header. You can change this to `PASETO` or any other string if you prefer:
```http
Authorization: PASETO v4.local.2w2...
```

## Standard PASETO Claims (Optional)

You can also enforce strict validation on top of expiration. If provided, `drf-pyseto` will ensure these claims match when verifying incoming tokens.

### `ISSUER`
**Default:** `None`
Sets the `iss` claim. Provides the identifier (usually a URL) of the server that issued the token.

### `AUDIENCE`
**Default:** `None`
Sets the `aud` claim. Provides the identifier of the intended recipient (the client application) for the token.
