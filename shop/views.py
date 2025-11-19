from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import User, Item, Category, Cart
from .serializers import UserSerializer, ItemSerializer, CategorySerializer, CartSerializer


class IsAdminOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'superadmin']


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'superadmin'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'me']:  # Added 'me' here
            return [permissions.AllowAny()]
        elif self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            return [IsSuperAdmin()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user info"""
        if request.user.is_authenticated:
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        return Response({'error': 'Not authenticated'}, status=401)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdminOrSuperAdmin()]


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdminOrSuperAdmin()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        queryset = Item.objects.all()
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['delete'])
    def clear(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response({'message': 'Cart cleared successfully'})