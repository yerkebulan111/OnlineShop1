from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ItemViewSet, CategoryViewSet, CartViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'items', ItemViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'cart', CartViewSet)

urlpatterns = [
    path('', include(router.urls)),
]