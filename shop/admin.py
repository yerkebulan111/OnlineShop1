from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Item, Category, Cart

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_active']
    list_filter = ['role', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'address')}),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'created_by', 'created_at']
    list_filter = ['category', 'created_at', 'created_by']
    search_fields = ['name', 'description']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'quantity', 'added_at']
    list_filter = ['user', 'added_at']