from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'SuperAdmin'),
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    stock = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.item.name} ({self.quantity})"

    class Meta:
        unique_together = ('user', 'item')