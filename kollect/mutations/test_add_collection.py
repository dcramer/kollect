from kollect.models import Collection


def test_add_collection(gql_client, default_user):
    executed = gql_client.execute(
        """
    mutation {
        addCollection(name:"My Games") {
            ok
            errors
            collection {id}
        }
    }""",
        user=default_user,
    )
    assert not executed.get("errors")
    resp = executed["data"]["addCollection"]
    assert resp["errors"] is None
    assert resp["ok"] is True

    collection = Collection.objects.get(id=resp["collection"]["id"])
    assert collection.name == "My Games"
    assert collection.created_by_id == default_user.id


def test_add_collection_with_description(gql_client, default_user):
    executed = gql_client.execute(
        """
    mutation {
        addCollection(name:"My Games", description:"Test") {
            ok
            errors
            collection {id}
        }
    }""",
        user=default_user,
    )
    assert not executed.get("errors")
    resp = executed["data"]["addCollection"]
    assert resp["errors"] is None
    assert resp["ok"] is True

    collection = Collection.objects.get(id=resp["collection"]["id"])
    assert collection.name == "My Games"
    assert collection.description == "Test"
    assert collection.created_by_id == default_user.id
