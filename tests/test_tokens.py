import pytest
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

from drf_pyseto.tokens import LEEWAY_SECONDS, create_token, decode_token


@pytest.mark.django_db
def test_valid_access_token_decodes():
    token = create_token(user_id=1, token_type="access", lifetime_seconds=60)
    payload = decode_token(token)
    assert payload["user_id"] == 1
    assert payload["typ"] == "access"


@pytest.mark.django_db
def test_expired_token_rejected():
    token = create_token(
        user_id=1, token_type="access", lifetime_seconds=-(LEEWAY_SECONDS + 1)
    )
    with pytest.raises(ImproperlyConfigured):
        decode_token(token)


@pytest.mark.django_db
def test_wrong_type_rejected():
    token = create_token(user_id=1, token_type="refresh", lifetime_seconds=60)
    payload = decode_token(token)
    assert payload["typ"] == "refresh"


@pytest.mark.django_db
def test_invalid_signature_rejected():
    token = create_token(user_id=1, token_type="access", lifetime_seconds=60)
    with override_settings(DRF_PYSETO={"KEY": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}):
        with pytest.raises(Exception):
            decode_token(token)
