import graphene
from django.db import IntegrityError, transaction

from kollect.models import Collection, Item
from kollect.schema import ItemNode


class AddItem(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        collection = graphene.UUID(required=True)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)
    item = graphene.Field(ItemNode)

    def mutate(self, info, name: str = None, collection: str = None):
        current_user = info.context.user
        if not current_user.is_authenticated:
            return AddItem(ok=False, errors=["Authentication required"])

        try:
            collection = Collection.objects.get(id=collection)
        except Collection.DoesNotExist:
            return AddItem(ok=False, errors=["Invalid Collection"])

        if collection.created_by_id != current_user.id:
            return AddItem(ok=False, errors=["Cannot edit this Collection"])

        try:
            with transaction.atomic():
                result = Item.objects.create(
                    name=name, collection=collection, created_by=current_user
                )
        except IntegrityError as exc:
            if "duplicate key" in str(exc):
                return AddItem(ok=False, errors=["Item already exists."])
            raise

        return AddItem(ok=True, item=result)
