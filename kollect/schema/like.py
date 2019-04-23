from graphene_django.types import DjangoObjectType

from kollect.models import Like


class LikeNode(DjangoObjectType):
    class Meta:
        model = Like
        name = "Like"
