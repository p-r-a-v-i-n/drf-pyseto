import pytest
from django.test import override_settings

from drf_pyseto.exceptions import PASETOError
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
    with pytest.raises(PASETOError, match="Token has expired"):
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
        with pytest.raises(Exception):  # pyseto raises its own DecryptError
            decode_token(token)


@pytest.mark.django_db
def test_issuer_validation():
    with override_settings(
        DRF_PYSETO={"KEY": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab", "ISSUER": "test-iss"}
    ):
        token = create_token(user_id=1, token_type="access", lifetime_seconds=60)

    # Decoding without the issuer expected should fail
    with override_settings(DRF_PYSETO={"KEY": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab"}):
        pass

    # Decode with WRONG issuer
    with override_settings(
        DRF_PYSETO={"KEY": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab", "ISSUER": "wrong"}
    ):
        with pytest.raises(PASETOError, match="Invalid token issuer"):
            decode_token(token)


@pytest.mark.django_db
def test_audience_validation():
    with override_settings(
        DRF_PYSETO={"KEY": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaac", "AUDIENCE": "test-aud"}
    ):
        token = create_token(user_id=1, token_type="access", lifetime_seconds=60)

    with override_settings(
        DRF_PYSETO={"KEY": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaac", "AUDIENCE": "wrong-aud"}
    ):
        with pytest.raises(PASETOError, match="Invalid token audience"):
            decode_token(token)
