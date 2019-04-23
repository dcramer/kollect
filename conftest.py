from uuid import UUID

import graphene.test
import pytest
from django.contrib.auth.models import AnonymousUser

from kollect import factories
from kollect.root_schema import schema


class Context(object):
    user = AnonymousUser()


class GqlClient(graphene.test.Client):
    def execute(self, query, user=None):
        context = Context()
        if user:
            context.user = user
        return super().execute(query, context=context)


@pytest.fixture
def gql_client(db):
    return GqlClient(schema)


@pytest.fixture
def default_user(db):
    user = factories.UserFactory(
        id=UUID("449c76aa-ad6a-46a8-b32b-91d965e3f462"),
        name="Reel Big Phish",
        email="reel.big.phish@example.com",
    )
    user.set_password("phish.reel.big")
    user.save()
    return user


@pytest.fixture
def default_collection(db, default_user):
    return factories.CollectionFactory.create(
        id=UUID("6960436f-53cd-4d00-bd5b-a293349e7d1f"),
        name="My Games",
        created_by=default_user,
        public=False,
    )


@pytest.fixture
def default_item(db, default_collection, default_user):
    return factories.ItemFactory.create(
        id=UUID("76111b88-301b-4620-9c93-7c6d28f0987b"),
        name="Unsettlers of Qatan",
        collection=default_collection,
        created_by=default_user,
    )
