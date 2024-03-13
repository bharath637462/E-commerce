from django.urls import path, include
from django.conf import settings
from rest_framework.routers import DefaultRouter

from ecommerce.views import ProductViewSet, CartViewSet, CategoryViewSet, CartProductsViewSet
from core.utills import get_api_url as api
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter(trailing_slash=False)
router.register(r'products', ProductViewSet, 'products')
router.register(r'carts', CartViewSet, 'carts')
router.register(r'categories', CategoryViewSet, 'categories')
router.register(r'cart_products', CartProductsViewSet, 'cart_products')

urlpatterns = [
    path(api(prefix='api'), include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)