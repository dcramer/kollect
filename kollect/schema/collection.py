import graphene
from graphene_django.types import DjangoObjectType

from kollect.models import Collection, Item


class CollectionNode(DjangoObjectType):
    num_items = graphene.Int(required=False)

    class Meta:
        name = "Collection"
        model = Collection

    def resolve_num_items(self, info):
        if not self.id:
            return 0
        if hasattr(self, "num_items"):
            return self.num_items
        return Item.objects.filter(collection=self.id).count()
