import graphene

from core.utills.graphql.types import CategoryType
from ecommerce.models import Category


class UpdateCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()

    category = graphene.Field(CategoryType)

    def mutate(self, info, id, name=None):
        category = Category.objects.get(id=id)
        if name is not None:
            category.name = name
        category.save()
        return UpdateCategoryMutation(category=category)