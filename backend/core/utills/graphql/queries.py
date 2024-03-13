import graphene
from graphene import List, String

from core.utills.graphql.types import CategoryType, ProductType, UserType
from ecommerce.models import Category, Product, User


class Query(graphene.ObjectType):

    #Category
    category = graphene.Field(CategoryType, id=graphene.ID(required=True))
    all_categories = graphene.List(CategoryType)

    def resolve_category(self, info, id):
        return Category.objects.get(id=id)

    def resolve_all_categories(self, info):
        return Category.objects.all()

    #Product
    product = graphene.Field(ProductType, id=graphene.ID())
    all_products = graphene.List(ProductType,  color=List(String), subCategory=List(String))

    def resolve_product(self, info, id):
        return Product.objects.get(id=id)

    def resolve_all_products(self, info, color=None, subCategory=None):
        queryset = Product.objects.all()
        if color:
            queryset = queryset.filter(colors__name__in=color).distinct()
        if subCategory:
            queryset = queryset.filter(sub_category__name__in=subCategory)

        return queryset

    #Users
    user = graphene.Field(UserType, id=graphene.ID(required=True))
    all_users = graphene.List(UserType)

    def resolve_user(self, info, id):
        return User.objects.get(id=id)

    def resolve_all_users(self, info):
        return User.objects.all()
