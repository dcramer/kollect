from kollect.models import Like


def test_add_like_as_creator(gql_client, default_user, default_item):
    executed = gql_client.execute(
        """
    mutation {
        addLike(item:"%s") {
            ok
            errors
        }
    }"""
        % (default_item.id,),
        user=default_user,
    )
    assert not executed.get("errors")
    resp = executed["data"]["addLike"]
    assert resp["errors"] is None
    assert resp["ok"] is True

    like = Like.objects.get(created_by=default_user, item=default_item)
    assert like.item_id == default_item.id
    assert like.created_by_id == default_user.id
