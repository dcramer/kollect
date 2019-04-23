from kollect.models import Item


def test_add_item(gql_client, default_user, default_collection):
    executed = gql_client.execute(
        """
    mutation {
        addItem(name:"Fight Club XI", collection:"%s") {
            ok
            errors
            item {id}
        }
    }"""
        % (default_collection.id,),
        user=default_user,
    )
    assert not executed.get("errors")
    resp = executed["data"]["addItem"]
    assert resp["errors"] is None
    assert resp["ok"] is True

    item = Item.objects.get(id=resp["item"]["id"])
    assert item.name == "Fight Club XI"
    assert item.created_by_id == default_user.id
    assert item.collection_id == default_collection.id
