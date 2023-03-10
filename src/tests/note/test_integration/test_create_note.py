import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from tests.factories.note import NoteFactory
from tests.factories.user import UserFactory


@pytest.mark.django_db
def test__create_note__success_case(api_client: APIClient) -> None:
    user = UserFactory.create()

    note = NoteFactory.create()
    note_data = {"name": note.name, "description": note.description}
    note.delete()

    api_client.force_authenticate(user)
    r = api_client.post(reverse("api:note-list"), data=note_data)
    r_data = r.json()

    assert r.status_code == status.HTTP_201_CREATED
    assert r_data["name"] == note_data["name"]
    assert r_data["description"] == note_data["description"]
    assert r_data["pk"]
    assert r_data["created_at"]


@pytest.mark.django_db
def test__create_note__without_data(api_client: APIClient) -> None:
    user = UserFactory.create()

    api_client.force_authenticate(user)
    r = api_client.post(reverse("api:note-list"))
    r_data = r.json()

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r_data["type"] == "validation_error"


@pytest.mark.django_db
def test__create_note__without_auth(api_client: APIClient) -> None:
    r = api_client.post(reverse("api:note-list"))
    r_data = r.json()

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert r_data["type"] == "authentication_error"


@pytest.mark.django_db
def test__create_note__without_name(api_client: APIClient) -> None:
    user = UserFactory.create()

    note = NoteFactory.create()
    note_data = {"description": note.description}
    note.delete()

    api_client.force_authenticate(user)
    r = api_client.post(reverse("api:note-list"), data=note_data)
    r_data = r.json()

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r_data["type"] == "validation_error"
