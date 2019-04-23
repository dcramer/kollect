import graphene

from kollect.models import Comment
from kollect.schema import ItemNode


class RemoveComment(graphene.Mutation):
    class Arguments:
        comment = graphene.UUID(required=True)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)
    item = graphene.Field(ItemNode)

    def mutate(self, info, comment: str = None):
        current_user = info.context.user
        if not current_user.is_authenticated:
            return RemoveComment(ok=False, errors=["Authentication required"])

        try:
            comment = Comment.objects.get(id=comment)
        except Comment.DoesNotExist:
            return RemoveComment(ok=False, errors=["Comment not found"])

        item = comment.item

        if (
            comment.created_by_id != current_user.id
            and item.created_by_id != current_user.id
        ):
            return RemoveComment(
                ok=False, errors=["Cannot remove comment from item"]
            )

        comment.delete()

        return RemoveComment(ok=True, item=item)
