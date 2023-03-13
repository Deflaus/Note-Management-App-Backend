import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from tests.factories.note import NoteFactory
from tests.factories.user import UserFactory


@pytest.mark.django_db
def test__get_note__own_note(api_client: APIClient) -> None:
    user = UserFactory.create()
    user_note = NoteFactory.create(user=user)

    api_client.force_authenticate(user)
    r = api_client.get(reverse("api:notes-detail", args=[user_note.pk]))
    r_data = r.json()

    assert r.status_code == status.HTTP_200_OK
    assert r_data["pk"] == user_note.pk
    assert r_data["name"] == user_note.name
    assert r_data["description"] == user_note.description


@pytest.mark.django_db
def test__get_note__other_note(api_client: APIClient) -> None:
    user1 = UserFactory.create()
    user2 = UserFactory.create()

    user2_note = NoteFactory.create(user=user2)

    api_client.force_authenticate(user1)
    r = api_client.get(reverse("api:notes-detail", args=[user2_note.pk]))

    assert r.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test__get_note__not_exists_note(api_client: APIClient) -> None:
    user = UserFactory.create()

    api_client.force_authenticate(user)
    r = api_client.get(reverse("api:notes-detail", args=[123]))

    assert r.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test__get_note__without_auth(api_client: APIClient) -> None:
    r = api_client.get(reverse("api:notes-detail", args=[123]))
    r_data = r.json()

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert r_data["type"] == "authentication_error"
