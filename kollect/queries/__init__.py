import graphene

from . import collections, comments, likes, me, users


class RootQuery(
    collections.Query,
    comments.Query,
    likes.Query,
    me.Query,
    users.Query,
    graphene.ObjectType,
):
    pass
