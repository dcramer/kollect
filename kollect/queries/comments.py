import graphene
from django.db.models import Q

from kollect.models import Comment, Follower
from kollect.schema import CommentNode
from kollect.utils.graphene import optimize_queryset


class Query(object):
    comments = graphene.List(
        CommentNode,
        id=graphene.UUID(),
        item=graphene.UUID(),
        created_by=graphene.UUID(),
    )

    def resolve_comments(
        self, info, id: str = None, item: str = None, created_by: str = None
    ):
        qs = Comment.objects.all()

        if not (id or item or created_by):
            return qs.none()

        current_user = info.context.user
        if not current_user.is_authenticated:
            qs = qs.filter(item__collection__public=True)
        else:
            qs = qs.filter(
                Q(item__collection__public=True)
                | Q(item__created_by=current_user)
                | Q(
                    item__created_by__in=Follower.objects.filter(
                        to_user=current_user
                    ).values("from_user_id")
                )
            )

        if id:
            qs = qs.filter(id=id)

        if item:
            qs = qs.filter(item=item)

        if created_by:
            qs = qs.filter(created_by=created_by)

        qs = qs.order_by("-created_at")

        qs = optimize_queryset(qs, info, "comments")

        return qs
