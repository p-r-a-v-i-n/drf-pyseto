SECRET_KEY = "test-secret"
DEBUG = True
USE_TZ = True
TIME_ZONE = "UTC"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "rest_framework",
    "drf_pyseto",
]

MIDDLEWARE = []

ROOT_URLCONF = "tests.urls"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

DRF_PYSETO = {
    "KEY": "0123456789abcdef0123456789abcdef",
    "ACCESS_LIFETIME": 300,
    "REFRESH_LIFETIME": 86400,
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "TOKEN_TYPE_CLAIM": "typ",
    "AUTH_HEADER_TYPE": "Bearer",
}
