import graphene
from django.db import transaction

from kollect.models import Collection
from kollect.schema import CollectionNode


class UpdateCollection(graphene.Mutation):
    class Arguments:
        collection = graphene.UUID(required=True)
        name = graphene.String(required=False)
        description = graphene.String(required=False)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)
    collection = graphene.Field(CollectionNode)

    def mutate(self, info, collection: str, name: str = None, description: str = None):
        current_user = info.context.user
        if not current_user.is_authenticated:
            return UpdateCollection(ok=False, errors=["Authentication required"])

        try:
            collection = Collection.objects.get(id=collection)
        except Collection.DoesNotExist:
            return UpdateCollection(ok=False, errors=["Invalid Collection"])

        if collection.created_by_id != current_user.id:
            return UpdateCollection(ok=False, errors=["Cannot edit this Collection"])

        with transaction.atomic():
            fields = []
            if name and name != collection.name:
                collection.name = name
                fields.append("name")
            if description and description != collection.description:
                collection.description = description
                fields.append("description")
            if fields:
                collection.save(update_fields=fields)
        return UpdateCollection(ok=True, collection=collection)
