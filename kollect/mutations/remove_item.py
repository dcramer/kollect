import graphene

from kollect.models import Item


class RemoveItem(graphene.Mutation):
    class Arguments:
        item = graphene.UUID(required=True)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, item: str = None):
        current_user = info.context.user
        if not current_user.is_authenticated:
            return RemoveItem(ok=False, errors=["Authentication required"])

        try:
            item = Item.objects.get(id=item)
        except Item.DoesNotExist:
            return RemoveItem(ok=False, errors=["Item not found"])

        if current_user.id != item.created_by_id:
            return RemoveItem(ok=False, errors=["Cannot remove like from item"])

        item.delete()

        return RemoveItem(ok=True, item=item)
