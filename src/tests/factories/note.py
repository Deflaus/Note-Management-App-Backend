import factory

from core.models import Note
from tests.factories.user import UserFactory


class NoteFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    name = factory.faker.Faker("name")
    description = factory.faker.Faker("name")

    class Meta:
        model = Note
