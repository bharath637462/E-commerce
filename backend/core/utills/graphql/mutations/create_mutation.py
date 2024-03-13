import graphene

from core.utills.graphql.types import CategoryType
from ecommerce.models import Category


class CreateCategoryMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    def mutate(self, info, name, description=None):
        category = Category(name=name)
        category.save()
        return CreateCategoryMutation(category=category)