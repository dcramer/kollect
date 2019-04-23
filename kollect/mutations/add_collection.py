import graphene
from django.db import IntegrityError, transaction

from kollect.models import Collection
from kollect.schema import CollectionNode


class AddCollection(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=False)

    ok = graphene.Boolean()
    errors = graphene.List(graphene.String)
    collection = graphene.Field(CollectionNode)

    def mutate(self, info, name: str, description: str = None):
        if not info.context.user.is_authenticated:
            return AddCollection(ok=False, errors=["Authentication required"])

        try:
            with transaction.atomic():
                result = Collection.objects.create(
                    name=name, description=description, created_by=info.context.user
                )
        except IntegrityError as exc:
            if "duplicate key" in str(exc):
                return AddCollection(ok=False, errors=["Collection already exists."])
            raise

        return AddCollection(ok=True, collection=result)
