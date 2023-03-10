import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from tests.factories.note import NoteFactory
from tests.factories.user import UserFactory


@pytest.mark.django_db
def test__delete_note__own_note(api_client: APIClient) -> None:
    user = UserFactory.create()
    user_note = NoteFactory.create(user=user)

    api_client.force_authenticate(user)
    r = api_client.delete(reverse("api:note-detail", args=[user_note.pk]))

    assert r.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test__delete_note__other_note(api_client: APIClient) -> None:
    user1 = UserFactory.create()
    user2 = UserFactory.create()

    user2_note = NoteFactory.create(user=user2)

    api_client.force_authenticate(user1)
    r = api_client.delete(reverse("api:note-detail", args=[user2_note.pk]))

    assert r.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test__delete_note__non_existent_note(api_client: APIClient) -> None:
    user = UserFactory.create()

    api_client.force_authenticate(user)
    r = api_client.delete(reverse("api:note-detail", args=[123]))

    assert r.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test__delete_note__without_auth(api_client: APIClient) -> None:
    r = api_client.delete(reverse("api:note-detail", args=[123]))
    r_data = r.json()

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert r_data["type"] == "authentication_error"
