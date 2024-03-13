from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ecommerce.models import Product, Cart, Category, User, CartProducts
from ecommerce.serializer import ProductSerializer, CartSerializer, CategorySerializer, CartProductsSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.filter(active=True)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]
    lookup_field = 'user'

    def get_queryset(self):
        # user = self.request.user
        user = User.objects.filter(active=True, email='bbk@gmail.com').first()
        queryset = Cart.objects.filter(active=True, user=user)
        return queryset

    def create(self, request, *args, **kwargs):
        user = request.data.get('user')
        if user:
            existing_cart = Cart.objects.filter(user=user, active=True).first()
            if existing_cart:
                # Update existing cart
                existing_cart.products.add(*request.data.get('products'))
                existing_cart.save()
                serializer = self.get_serializer(existing_cart)
                return Response(serializer.data)
        return super().create(request, *args, **kwargs)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class CartProductsViewSet(ModelViewSet):
    queryset = CartProducts.objects.filter(active=True)
    serializer_class = CartProductsSerializer
    permission_classes = [AllowAny]
    lookup_field = 'products'

    def get_queryset(self):
        user = self.request.user
        cart_id = Cart.objects.filter(user=user).first().id
        queryset = CartProducts.objects.filter(active=True, cart=cart_id)
        print(queryset)
        return queryset