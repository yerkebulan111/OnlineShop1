from rest_framework import serializers
from .models import User, Item, Category, Cart


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'phone', 'address', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data.get('role', 'user'),
            phone=validated_data.get('phone', ''),
            address=validated_data.get('address', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class ItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'price', 'category', 'category_name', 'image', 'stock', 'created_by',
                  'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class CartSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_price = serializers.DecimalField(source='item.price', max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'item', 'item_name', 'item_price', 'quantity', 'total_price', 'added_at']
        read_only_fields = ['added_at']

    def get_total_price(self, obj):
        return obj.item.price * obj.quantity