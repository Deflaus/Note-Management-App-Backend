import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from tests.factories.user import UserFactory


@pytest.mark.django_db
def test__sign_out__success_case(api_client: APIClient) -> None:
    user = UserFactory.create()
    token, _ = Token.objects.get_or_create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

    r = api_client.post(reverse("api:auth-sign-out"))

    assert r.status_code == status.HTTP_204_NO_CONTENT
    assert not Token.objects.filter(user=user)


@pytest.mark.django_db
def test__sign_out__error_case(api_client: APIClient) -> None:
    r = api_client.post(reverse("api:auth-sign-out"))
    r_data = r.json()

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert r_data["type"] == "authentication_error"
