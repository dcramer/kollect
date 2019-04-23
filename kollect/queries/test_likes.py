from kollect.models import Like


def test_likes_for_item(gql_client, default_user, default_item):
    like = Like.objects.create(created_by=default_user, item=default_item)

    executed = gql_client.execute(
        """{ likes(item:"%s") { id } }""" % (default_item.id,), user=default_user
    )
    assert not executed.get("errors")
    assert executed["data"]["likes"] == [{"id": str(like.id)}]
