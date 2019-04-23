from kollect.models import Comment


def test_add_comment_as_creator(gql_client, default_user, default_item):
    executed = gql_client.execute(
        """
    mutation {
        addComment(text:"Hi :)", item:"%s") {
            ok
            errors
            comment {id}
        }
    }"""
        % (default_item.id,),
        user=default_user,
    )
    assert not executed.get("errors")
    resp = executed["data"]["addComment"]
    assert resp["errors"] is None
    assert resp["ok"] is True

    comment = Comment.objects.get(id=resp["comment"]["id"])
    assert comment.text == "Hi :)"
    assert comment.item_id == default_item.id
    assert comment.created_by_id == default_user.id
