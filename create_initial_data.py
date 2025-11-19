import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OnlineShop1.settings')
django.setup()

from shop.models import User, Category, Item

# Create superadmin
superadmin, created = User.objects.get_or_create(
    username='super_admin',
    defaults={
        'role': 'superadmin',
        'email': 'superadmin@example.com',
        'is_staff': True,
        'is_superuser': True
    }
)
if created:
    superadmin.set_password('123')
    superadmin.save()
    print("✅ Superadmin created! (username: super_admin, password: 123)")
else:
    print("ℹ️ Superadmin already exists")

# Create admin (seller)
admin, created = User.objects.get_or_create(
    username='admin_seller',
    defaults={
        'role': 'admin',
        'email': 'admin@example.com'
    }
)
if created:
    admin.set_password('123')
    admin.save()
    print("✅ Admin created! (username: admin_seller, password: 123)")
else:
    print("ℹ️ Admin already exists")

# Create default user
user, created = User.objects.get_or_create(
    username='GalymBartay',
    defaults={
        'role': 'user',
        'email': 'galym@example.com'
    }
)
if created:
    user.set_password('12345678')
    user.save()
    print("✅ User GalymBartay created!")
else:
    print("ℹ️ User GalymBartay already exists")

# Create categories for socks
categories_data = [
    {'name': 'Спортивные носки', 'description': 'Носки для спорта и активного отдыха'},
    {'name': 'Классические носки', 'description': 'Носки для повседневной носки'},
    {'name': 'Теплые носки', 'description': 'Зимние и теплые носки'},
    {'name': 'Детские носки', 'description': 'Носки для детей'},
]

categories = {}
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={'description': cat_data['description']}
    )
    categories[cat_data['name']] = category
    if created:
        print(f"✅ Category '{category.name}' created!")

# Create sample items (2 per category)
items_data = [
    # Спортивные носки
    {
        'name': 'Nike Спортивные носки Pro',
        'description': 'Высокопроизводительные носки для бега и тренировок',
        'price': 2500,
        'category': 'Спортивные носки',
        'stock': 50
    },
    {
        'name': 'Adidas Performance носки',
        'description': 'Дышащие носки с технологией Climacool',
        'price': 2200,
        'category': 'Спортивные носки',
        'stock': 45
    },
    # Классические носки
    {
        'name': 'Классические черные носки',
        'description': 'Элегантные носки для офиса и деловых встреч',
        'price': 1500,
        'category': 'Классические носки',
        'stock': 100
    },
    {
        'name': 'Классические серые носки',
        'description': 'Универсальные носки на каждый день',
        'price': 1400,
        'category': 'Классические носки',
        'stock': 80
    },
    # Теплые носки
    {
        'name': 'Шерстяные зимние носки',
        'description': 'Теплые носки из натуральной шерсти',
        'price': 3000,
        'category': 'Теплые носки',
        'stock': 60
    },
    {
        'name': 'Махровые носки',
        'description': 'Мягкие и теплые носки для дома',
        'price': 1800,
        'category': 'Теплые носки',
        'stock': 70
    },
    # Детские носки
    {
        'name': 'Детские носки с мишками',
        'description': 'Яркие носки с рисунками для детей 3-7 лет',
        'price': 1000,
        'category': 'Детские носки',
        'stock': 90
    },
    {
        'name': 'Детские носки радуга',
        'description': 'Разноцветные носки для детей 5-10 лет',
        'price': 1100,
        'category': 'Детские носки',
        'stock': 85
    },
]

for item_data in items_data:
    category = categories[item_data['category']]
    item, created = Item.objects.get_or_create(
        name=item_data['name'],
        defaults={
            'description': item_data['description'],
            'price': item_data['price'],
            'category': category,
            'stock': item_data['stock'],
            'created_by': admin  # Items created by admin
        }
    )
    if created:
        print(f"✅ Item '{item.name}' created!")

print("\n✅ All initial data created successfully!")
print("\nAccounts created:")
print("- Superadmin: super_admin / 123")
print("- Admin: admin_seller / 123")
print("- User: GalymBartay / 12345678")