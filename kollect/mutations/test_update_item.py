from kollect import factories
from kollect.models import Item


def test_update_item_with_collections(
    gql_client, default_collection, default_item, default_user
):
    new_collection = factories.CollectionFactory.create(created_by=default_user)
    executed = gql_client.execute(
        """
    mutation {
        updateItem(item:"%s", collection:"%s") {
            ok
            errors
            item { id }
        }
    }"""
        % (str(default_item.id), str(new_collection.id)),
        user=default_user,
    )
    assert not executed.get("errors")
    resp = executed["data"]["updateItem"]
    assert resp["errors"] is None
    assert resp["ok"] is True

    item = Item.objects.get(id=default_item.id)
    assert item.collection_id == new_collection.id
