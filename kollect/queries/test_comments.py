from kollect.models import Comment


def test_comments_for_item(gql_client, default_user, default_item):
    comment = Comment.objects.create(
        created_by=default_user, item=default_item, text="Hi :)"
    )

    executed = gql_client.execute(
        """{ comments(item:"%s") { id } }""" % (default_item.id,), user=default_user
    )
    assert not executed.get("errors")
    assert executed["data"]["comments"] == [{"id": str(comment.id)}]
