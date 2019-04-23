import graphene
from graphene_django.types import DjangoObjectType

from kollect.models import Item, ItemImage


class ItemImageNode(DjangoObjectType):
    url = graphene.String()

    class Meta:
        name = "ItemImage"
        model = ItemImage
        only_fields = ("width", "height")

    def resolve_url(self, args):
        if not self.file:
            return None
        url = self.file.url
        if not url.startswith(("http:", "https:")):
            if not url.startswith("/"):
                url = "/" + url
            url = args.context.build_absolute_uri(url)
        return url


class ItemNode(DjangoObjectType):
    image = ItemImageNode()

    class Meta:
        name = "Item"
        model = Item
