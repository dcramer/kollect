import graphene
from django.db import transaction

from kollect.models import Collection, Item
from kollect.schema import ItemNode


class UpdateItem(graphene.Mutation):
    class Arguments:
        item = graphene.UUID(required=True)
        name = graphene.String(required=False)
        collection = graphene.UUID(required=False)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)
    item = graphene.Field(ItemNode)

    def mutate(self, info, item: str, name: str = None, collection: str = None):
        current_user = info.context.user
        if not current_user.is_authenticated:
            return UpdateItem(ok=False, errors=["Authentication required"])

        try:
            item = Item.objects.get(id=item)
        except Item.DoesNotExist:
            return UpdateItem(ok=False, errors=["Invalid Item"])

        if item.created_by_id != current_user.id:
            return UpdateItem(ok=False, errors=["Cannot edit this Item"])

        if collection:
            try:
                collection = Collection.objects.get(id=collection)
            except Collection.DoesNotExist:
                return UpdateItem(ok=False, errors=["Invalid Collection"])
            if collection.created_by_id != current_user.id:
                return UpdateItem(ok=False, errors=["Cannot reference this Collection"])

        with transaction.atomic():
            fields = []
            if name and name != collection.name:
                item.name = name
                fields.append("name")
            if collection and collection != item.collection_id:
                item.collection = collection
                fields.append("collection")
            if fields:
                item.save(update_fields=fields)

        return UpdateItem(ok=True, item=item)
