import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from tests.factories.user import UserFactory
from tests.utils import get_random_password


@pytest.mark.django_db
def test__sign_in__success_case(api_client: APIClient) -> None:
    user = UserFactory.create()
    password = get_random_password()
    user.set_password(password)
    user.save()

    user_data = {"username": user.username, "password": password}

    r = api_client.post(reverse("api:auth-sign-in"), data=user_data)
    r_data = r.json()

    assert r.status_code == status.HTTP_200_OK
    assert r_data["username"] == user_data["username"]
    assert r_data["is_active"] is True
    assert r_data["token"]


@pytest.mark.django_db
def test__sign_in__without_data(api_client: APIClient) -> None:
    r = api_client.post(reverse("api:auth-sign-in"))
    r_data = r.json()

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r_data["type"] == "validation_error"


@pytest.mark.django_db
def test__sign_in__invalid_password(api_client: APIClient) -> None:
    user = UserFactory.create()
    password = get_random_password()
    user.set_password(password)
    user.save()

    user_data = {"username": user.username, "password": "other_password"}

    r = api_client.post(reverse("api:auth-sign-in"), data=user_data)
    r_data = r.json()

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert r_data["type"] == "authentication_error"


@pytest.mark.django_db
def test__sign_in__invalid_username(api_client: APIClient) -> None:
    user = UserFactory.create()
    password = get_random_password()
    user.set_password(password)
    user.save()

    user_data = {"username": "other_username", "password": password}

    r = api_client.post(reverse("api:auth-sign-in"), data=user_data)
    r_data = r.json()

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert r_data["type"] == "authentication_error"
