import graphene

from ecommerce.models import Category


class DeleteCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            Category.objects.get(id=id).delete()
            success = True
        except Category.DoesNotExist:
            success = False
        return DeleteCategoryMutation(success=success)