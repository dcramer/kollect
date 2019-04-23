import graphene

import kollect.mutations
import kollect.queries

schema = graphene.Schema(
    query=kollect.queries.RootQuery, mutation=kollect.mutations.RootMutation
)
