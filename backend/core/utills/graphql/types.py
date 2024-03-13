from graphene_django import DjangoObjectType
from graphene import List, ObjectType, String
from ecommerce.models import Category, Product, Color, SubCategory, User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ['name']


class ColorsType(DjangoObjectType):
    class Meta:
        model = Color
        fields = ['name']


class SubCategoryType(DjangoObjectType):
    class Meta:
        model = SubCategory
        fields = ['name']

class RatingType(DjangoObjectType):
    class Meta:
        model = SubCategory
        fields = ['name']


class ProductType(DjangoObjectType):
    colors = List(ColorsType)
    sub_category = List(SubCategoryType)

    class Meta:
        model = Product
        fields = ['name', 'colors', 'sub_category']

    def resolve_colors(self, info):
        return self.colors.all()
