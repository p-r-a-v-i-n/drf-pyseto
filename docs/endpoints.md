# API Endpoints

Once you have included the `drf_pyseto.urls` in your URL routing Configuration, `drf-pyseto` provides two standard endpoints out of the box.

## 1. Obtain Tokens

This endpoint accepts a `username` and `password` and returns an encrypted PASETO access token and refresh token.

**Request:**

```http
POST /api/auth/token/ HTTP/1.1
Content-Type: application/json

{
    "username": "admin",
    "password": "supersecurepassword"
}
```

**Response:**

Unlike JSON Web Tokens (JWT) which consist of three base64-encoded segments separated by a period, PASETO `v4.local` tokens are fully encrypted payloads. They always start with `v4.local.`.

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "access": "v4.local.2w2V5Knt1l0Jm4a9xS0S0z01v4Z-S1A6K9z1W2n_6s0lI-102K8P2K_W-b3v1K_4Z9X0S30c_W3K80a-9Y5b_L2A1v-4W9",
    "refresh": "v4.local.6d2S9Hyt0k0Jm7b8xW0F1w34v8L-W9K0M2z1Q9m_4a5pI-305L1T6V_V-b3z2A_4Q2Z0T15p_L4M7A0k-8U3c_Q8M4c-6T0"
}
```

## 2. Refresh Access Token

Access tokens typically expire quickly to enforce security boundaries. When an access token expires, clients can use their longer-lived `refresh` token to obtain a new access token without needing the user's password.

**Request:**

```http
POST /api/auth/token/refresh/ HTTP/1.1
Content-Type: application/json

{
    "refresh": "v4.local.6d2S9Hyt0k0Jm7b8xW0F1w34v8L-W9K0M2z1Q9m_4a5pI-305L1T6V_V-b3z2A_4Q2Z0T15p_L4M7A0k-8U3c_Q8M4c-6T0"
}
```

**Response:**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "access": "v4.local.4q5Y9Olk9a2Bn6x1pV6E4y21r5X-A3D9H7z5V3l_8c2xN-201H9M3X_M-h9e8X_4Y1T8Q50e_A9K1P6u-7O5a_R2L9x-8V4"
}
```

## Authorization Header Usage

To authenticate subsequent requests to your protected REST endpoints, you must include the access token in your request headers. By default, `drf-pyseto` looks for the `Bearer` token type:

```http
GET /api/protected-resource/ HTTP/1.1
Authorization: Bearer v4.local.2w2V5Knt1l0Jm4a9...
```
