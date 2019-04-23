import graphene
from django.db.models import Count

from kollect.models import Collection
from kollect.schema import CollectionNode
from kollect.utils.graphene import optimize_queryset


def fix_collections_query(queryset, selected_fields, **kwargs):
    if "items.image" in selected_fields:
        queryset = queryset.prefetch_related("items__image")
    if "numItems" in selected_fields:
        queryset = queryset.annotate(num_items=Count("items"))
    return queryset


class Query(object):
    collections = graphene.List(
        CollectionNode,
        id=graphene.UUID(),
        query=graphene.String(),
        created_by=graphene.UUID(),
    )

    def resolve_collections(
        self,
        info,
        id: str = None,
        query: str = None,
        created_by: str = None,
    ):
        qs = Collection.objects.all().distinct()

        if not (id or created_by):
            return qs.none()

        if id:
            qs = qs.filter(id=id)

        if query:
            qs = qs.filter(name__istartswith=query)

        if created_by:
            qs = qs.filter(created_by=created_by)

        qs = qs.order_by("name")

        qs = optimize_queryset(qs, info, "collections", fix_collections_query)

        return qs
