import graphene

from core.utills.graphql.mutations_list import Mutation
from core.utills.graphql.queries import Query

schema = graphene.Schema(query=Query, mutation=Mutation)