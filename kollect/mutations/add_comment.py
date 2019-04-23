import graphene
from django.db import IntegrityError, transaction

from kollect.models import Comment, Follower, Item
from kollect.schema import CommentNode, ItemNode


class AddComment(graphene.Mutation):
    class Arguments:
        item = graphene.UUID(required=True)
        text = graphene.String(required=True)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)
    comment = graphene.Field(CommentNode)
    item = graphene.Field(ItemNode)

    def mutate(self, info, item: str = None, text: str = None):
        current_user = info.context.user
        if not current_user.is_authenticated:
            return AddComment(ok=False, errors=["Authentication required"])

        try:
            item = Item.objects.get(id=item)
        except Item.DoesNotExist:
            return AddComment(ok=False, errors=["Item not found"])

        if current_user.id == item.created_by_id:
            pass
        elif Follower.objects.filter(
            to_user=current_user, from_user_id=item.created_by_id
        ):
            pass
        else:
            return AddComment(ok=False, errors=["Cannot add comment to item"])

        try:
            with transaction.atomic():
                result = Comment.objects.create(
                    item=item, text=text, created_by=info.context.user
                )

        except IntegrityError as exc:
            if "duplicate key" in str(exc):
                return AddComment(ok=False, errors=["Comment already exists."])
            raise

        return AddComment(ok=True, comment=result, item=item)
