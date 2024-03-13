import graphene

from core.utills.graphql.mutations.create_mutation import CreateCategoryMutation

from core.utills.graphql.mutations.update_mutation import UpdateCategoryMutation

from core.utills.graphql.mutations.delete_mutation import DeleteCategoryMutation


class Mutation(graphene.ObjectType):

    # Category
    create_category = CreateCategoryMutation.Field()
    update_category = UpdateCategoryMutation.Field()
    delete_category = DeleteCategoryMutation.Field()



