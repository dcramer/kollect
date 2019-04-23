import factory

from .. import models
from .user import UserFactory


class ItemFactory(factory.django.DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = models.Item
