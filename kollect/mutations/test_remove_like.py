from kollect.models import Like


def test_remove_like_as_creator(gql_client, default_user, default_item):
    Like.objects.create(created_by=default_user, item=default_item)

    executed = gql_client.execute(
        """
    mutation {
        removeLike(item:"%s") {
            ok
            errors
        }
    }"""
        % (default_item.id,),
        user=default_user,
    )
    assert not executed.get("errors")
    resp = executed["data"]["removeLike"]
    assert resp["errors"] is None
    assert resp["ok"] is True

    assert not Like.objects.filter(
        created_by=default_user, item=default_item
    ).exists()


def test_remove_like_as_creator_noop(gql_client, default_user, default_item):
    Like.objects.create(created_by=default_user, item=default_item)

    executed = gql_client.execute(
        """
    mutation {
        removeLike(item:"%s") {
            ok
            errors
        }
    }"""
        % (default_item.id,),
        user=default_user,
    )
    assert not executed.get("errors")
    resp = executed["data"]["removeLike"]
    assert resp["errors"] is None
    assert resp["ok"] is True

    assert not Like.objects.filter(
        created_by=default_user, item=default_item
    ).exists()
