from kollect.models import Collection


def test_update_collection(gql_client, default_collection, default_user):
    executed = gql_client.execute(
        """
    mutation {
        updateCollection(collection:"%s", name:"Updated Collection") {
            ok
            errors
            collection { id }
        }
    }"""
        % (str(default_collection.id),),
        user=default_user,
    )
    assert not executed.get("errors")
    resp = executed["data"]["updateCollection"]
    assert resp["errors"] is None
    assert resp["ok"] is True

    collection = Collection.objects.get(id=resp["collection"]["id"])
    assert collection.name == "Updated Collection"


def test_update_collection_with_description(
    gql_client, default_collection, default_user
):
    executed = gql_client.execute(
        """
    mutation {
        updateCollection(collection:"%s", description:"Test") {
            ok
            errors
            collection { id }
        }
    }"""
        % (str(default_collection.id),),
        user=default_user,
    )
    assert not executed.get("errors")
    resp = executed["data"]["updateCollection"]
    assert resp["errors"] is None
    assert resp["ok"] is True

    collection = Collection.objects.get(id=resp["collection"]["id"])
    assert collection.description == "Test"
