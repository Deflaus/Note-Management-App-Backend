import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from tests.factories.note import NoteFactory
from tests.factories.user import UserFactory


def new_note_name_and_description() -> dict[str, str]:
    return {"name": "New name", "description": "New description"}


def new_note_description() -> dict[str, str]:
    return {"description": "New description"}


def new_note_name() -> dict[str, str]:
    return {"name": "New name"}


@pytest.mark.django_db
def test__update_note__own_note_name_and_description(api_client: APIClient) -> None:
    user = UserFactory.create()
    user_note = NoteFactory.create(user=user)

    data = new_note_name_and_description()

    api_client.force_authenticate(user)
    r = api_client.patch(reverse("api:notes-detail", args=[user_note.pk]), data=data)
    r_data = r.json()

    assert r.status_code == status.HTTP_200_OK
    assert r_data["pk"] == user_note.pk
    assert r_data["name"] == data["name"]
    assert r_data["description"] == data["description"]


@pytest.mark.django_db
def test__update_note__own_note_description(api_client: APIClient) -> None:
    user = UserFactory.create()
    user_note = NoteFactory.create(user=user)

    data = new_note_description()

    api_client.force_authenticate(user)
    r = api_client.patch(reverse("api:notes-detail", args=[user_note.pk]), data=data)
    r_data = r.json()

    assert r.status_code == status.HTTP_200_OK
    assert r_data["pk"] == user_note.pk
    assert r_data["name"] == user_note.name
    assert r_data["description"] == data["description"]


@pytest.mark.django_db
def test__update_note__own_note_name(api_client: APIClient) -> None:
    user = UserFactory.create()
    user_note = NoteFactory.create(user=user)

    data = new_note_name()

    api_client.force_authenticate(user)
    r = api_client.patch(reverse("api:notes-detail", args=[user_note.pk]), data=data)
    r_data = r.json()

    assert r.status_code == status.HTTP_200_OK
    assert r_data["pk"] == user_note.pk
    assert r_data["name"] == data["name"]
    assert r_data["description"] == user_note.description


@pytest.mark.django_db
def test__update_note__other_note(api_client: APIClient) -> None:
    user1 = UserFactory.create()
    user2 = UserFactory.create()
    user2_note = NoteFactory.create(user=user2)

    data = new_note_name_and_description()

    api_client.force_authenticate(user1)
    r = api_client.patch(reverse("api:notes-detail", args=[user2_note.pk]), data=data)

    assert r.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test__update_note__non_existent_note(api_client: APIClient) -> None:
    user = UserFactory.create()

    api_client.force_authenticate(user)
    r = api_client.patch(reverse("api:notes-detail", args=[123]), data=new_note_name_and_description())

    assert r.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test__update_note__without_auth(api_client: APIClient) -> None:
    r = api_client.patch(reverse("api:notes-detail", args=[123]))
    r_data = r.json()

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert r_data["type"] == "authentication_error"
