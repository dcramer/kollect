from kollect.models import Comment


def test_remove_comment_as_creator(gql_client, default_user, default_item):
    comment = Comment.objects.create(
        created_by=default_user, item=default_item, text="test"
    )

    executed = gql_client.execute(
        """
    mutation {
        removeComment(comment:"%s") {
            ok
            errors
        }
    }"""
        % (comment.id,),
        user=default_user,
    )
    assert not executed.get("errors")
    resp = executed["data"]["removeComment"]
    assert resp["errors"] is None
    assert resp["ok"] is True

    assert not Comment.objects.filter(id=comment.id).exists()
