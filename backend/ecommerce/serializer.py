from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ecommerce.models import Product, Cart, Category, CartProducts


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'image', 'price')


class CartSerializer(ModelSerializer):
    product_details = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('user', 'products', 'product_details')

    def get_product_details(self, obj):
        return [{'id': cart_product.products.id, 'name': cart_product.products.name, 'price': cart_product.products.price, 'img': 'http://127.0.0.1:8000/' + str(cart_product.products.image.url), 'count': cart_product.count} for cart_product in
                obj.cart_products.all()]


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class CartProductsSerializer(ModelSerializer):
    class Meta:
        model = CartProducts
        fields = ('count', 'products')