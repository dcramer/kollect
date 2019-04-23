import graphene

from kollect.models import Follower, Item, Like
from kollect.schema import ItemNode


class RemoveLike(graphene.Mutation):
    class Arguments:
        item = graphene.UUID(required=True)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)
    item = graphene.Field(ItemNode)

    def mutate(self, info, item: str = None):
        current_user = info.context.user
        if not current_user.is_authenticated:
            return RemoveLike(ok=False, errors=["Authentication required"])

        try:
            item = Item.objects.get(id=item)
        except Item.DoesNotExist:
            return RemoveLike(ok=False, errors=["Item not found"])

        if current_user.id == item.created_by_id:
            pass
        elif Follower.objects.filter(
            to_user=current_user, from_user_id=item.created_by_id
        ):
            pass
        else:
            return RemoveLike(ok=False, errors=["Cannot remove like from item"])

        Like.objects.filter(item=item, created_by=info.context.user).delete()

        return RemoveLike(ok=True, item=item)
