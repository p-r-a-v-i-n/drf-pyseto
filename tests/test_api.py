import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APIRequestFactory

from drf_pyseto.authentication import PASETOAuthentication
from drf_pyseto.tokens import create_access_token, create_refresh_token


@pytest.mark.django_db
def test_token_obtain_and_refresh_flow():
    get_user_model().objects.create_user(username="alice", password="password")
    client = APIClient()

    res = client.post(
        "/token/", {"username": "alice", "password": "password"}, format="json"
    )
    assert res.status_code == 200
    assert "access" in res.data
    assert "refresh" in res.data

    res2 = client.post(
        "/token/refresh/", {"refresh": res.data["refresh"]}, format="json"
    )
    assert res2.status_code == 200
    assert "access" in res2.data


@pytest.mark.django_db
def test_invalid_credentials():
    get_user_model().objects.create_user(username="bob", password="password")
    client = APIClient()
    res = client.post(
        "/token/", {"username": "bob", "password": "wrong"}, format="json"
    )
    assert res.status_code == 401


@pytest.mark.django_db
def test_refresh_token_rejected_by_authentication():
    user = get_user_model().objects.create_user(username="cora", password="password")
    refresh = create_refresh_token(user.id)

    factory = APIRequestFactory()
    request = factory.get("/protected/", HTTP_AUTHORIZATION=f"Bearer {refresh}")
    auth = PASETOAuthentication()

    with pytest.raises(Exception):
        auth.authenticate(request)


@pytest.mark.django_db
def test_refresh_with_access_token_fails():
    user = get_user_model().objects.create_user(username="dan", password="password")
    access = create_access_token(user.id)

    client = APIClient()
    res = client.post("/token/refresh/", {"refresh": access}, format="json")
    assert res.status_code == 401
