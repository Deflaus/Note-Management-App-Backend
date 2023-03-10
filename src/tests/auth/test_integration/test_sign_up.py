import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from tests.factories.user import UserFactory
from tests.utils import get_random_password


@pytest.mark.django_db
def test__sign_up__success_case(api_client: APIClient) -> None:
    user = UserFactory.create()
    user_data = {"username": user.username, "password": get_random_password()}
    user.delete()

    r = api_client.post(reverse("api:auth-sign-up"), data=user_data)
    r_data = r.json()

    assert r.status_code == status.HTTP_201_CREATED
    assert r_data["username"] == user_data["username"]
    assert r_data["is_active"] is True
    assert r_data["token"]


@pytest.mark.django_db
def test__sign_up__without_data(api_client: APIClient) -> None:
    r = api_client.post(reverse("api:auth-sign-up"))
    r_data = r.json()

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r_data["type"] == "validation_error"


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("username", "password"),
    [
        ("some username with spaces", get_random_password()),
        ("some_username", "123"),
    ],
    ids=["invalid_username", "invalid_password"],
)
def test__sign_up__invalid_input(api_client: APIClient, username: str, password: str) -> None:
    user_data = {
        "username": username,
        "password": password,
    }

    r = api_client.post(reverse("api:auth-sign-up"), data=user_data)
    r_data = r.json()

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r_data["type"] == "validation_error"
