from kollect import factories
from kollect.models import Collection


def test_remove_collection(gql_client, default_user):
    collection = factories.CollectionFactory.create(created_by=default_user)

    executed = gql_client.execute(
        """
    mutation {
        removeCollection(collection:"%s") {
            ok
            errors
        }
    }"""
        % (str(collection.id),),
        user=default_user,
    )
    assert not executed.get("errors")
    resp = executed["data"]["removeCollection"]
    assert resp["errors"] is None
    assert resp["ok"] is True

    assert not Collection.objects.filter(id=collection.id).exists()


def test_remove_collection_invalid_user(gql_client, default_user):
    collection = factories.CollectionFactory.create()

    executed = gql_client.execute(
        """
    mutation {
        removeCollection(collection:"%s") {
            ok
            errors
        }
    }"""
        % (str(collection.id),),
        user=default_user,
    )
    assert not executed.get("errors")
    resp = executed["data"]["removeCollection"]
    assert resp["ok"] is False
    assert resp["errors"]

    assert Collection.objects.filter(id=collection.id).exists()
