import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Note
from tests.factories.note import NoteFactory
from tests.factories.user import UserFactory


def check_target_user_notes(response_notes: list[dict], target_user_notes: list[Note]) -> None:
    for r_note, user_note in zip(response_notes, target_user_notes):
        assert r_note["pk"] == user_note.pk


def check_other_user_notes(response_notes: list[dict], other_user_notes: list[Note]) -> None:
    for r_note in response_notes:
        for user_note in other_user_notes:
            assert r_note["pk"] != user_note.pk


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("user1_notes_count", "user2_notes_count"),
    [
        (10, 5),
        (0, 0),
        (10, 0),
        (0, 5),
    ],
    ids=["both_user_have_notes", "both_users_have_no_notes", "only_user1_have_notes", "only_user2_have_notes"],
)
def test__get_note_list__success_case(api_client: APIClient, user1_notes_count, user2_notes_count) -> None:
    user1 = UserFactory.create()
    user2 = UserFactory.create()

    user1_notes = NoteFactory.create_batch(user1_notes_count, user=user1)
    user2_notes = NoteFactory.create_batch(user2_notes_count, user=user2)

    api_client.force_authenticate(user1)
    r = api_client.get(reverse("api:note-list"))
    r_data = r.json()

    assert r.status_code == status.HTTP_200_OK
    assert len(r_data) == len(user1_notes)
    check_target_user_notes(r_data, user1_notes)
    check_other_user_notes(r_data, user2_notes)


@pytest.mark.django_db
def test__get_note_list__without_auth(api_client: APIClient) -> None:
    r = api_client.get(reverse("api:note-list"))
    r_data = r.json()

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert r_data["type"] == "authentication_error"
