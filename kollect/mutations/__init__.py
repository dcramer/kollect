import graphene

from .add_collection import AddCollection
from .add_comment import AddComment
from .add_item import AddItem
from .add_like import AddLike
from .follow import Follow
from .login import Login
from .remove_collection import RemoveCollection
from .remove_comment import RemoveComment
from .remove_item import RemoveItem
from .remove_like import RemoveLike
from .unfollow import Unfollow
from .update_collection import UpdateCollection
from .update_item import UpdateItem


class RootMutation(graphene.ObjectType):
    addCollection = AddCollection.Field()
    addComment = AddComment.Field()
    addLike = AddLike.Field()
    addItem = AddItem.Field()
    follow = Follow.Field()
    login = Login.Field()
    removeCollection = RemoveCollection.Field()
    removeComment = RemoveComment.Field()
    removeItem = RemoveItem.Field()
    removeLike = RemoveLike.Field()
    unfollow = Unfollow.Field()
    updateCollection = UpdateCollection.Field()
    updateItem = UpdateItem.Field()
