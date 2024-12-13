from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150,unique=True, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return self.username

class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True)  # Индекс для быстрого поиска по имени
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    category = models.ForeignKey('Category', related_name='products', on_delete=models.CASCADE, db_index=True)  # Индекс для поиска по категории
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
        ]


    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', related_name='subcategories', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['parent']),
        ]

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey('User', related_name='orders', on_delete=models.CASCADE, db_index=True)
    order_status = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
        ]


    def __str__(self):
        return f'Order {self.id}'

class OrderItem(models.Model):
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE, db_index=True)
    product = models.ForeignKey('Product', related_name='order_items', on_delete=models.CASCADE, db_index=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['product']),
        ]


    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

class ShoppingCart(models.Model):
    user = models.OneToOneField('User', related_name='cart', on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'Cart of {self.user.username}'

class CartItem(models.Model):
    cart = models.ForeignKey('ShoppingCart', related_name='items', on_delete=models.CASCADE, db_index=True)
    product = models.ForeignKey('Product', related_name='cart_items', on_delete=models.CASCADE, db_index=True)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['cart']),
            models.Index(fields=['product']),
        ]


    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

class Payment(models.Model):
    order = models.ForeignKey('Order', related_name='payments', on_delete=models.CASCADE, db_index=True)
    payment_method = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Payment for Order {self.order.id}'

class Review(models.Model):
    product = models.ForeignKey('Product', related_name='reviews', on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey('User', related_name='reviews', on_delete=models.CASCADE, db_index=True)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f'Review by {self.user.username}'

class Wishlist(models.Model):
    user = models.ForeignKey('User', related_name='wishlists', on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Wishlist of {self.user.username}'

class WishlistItem(models.Model):
    wishlist = models.ForeignKey('Wishlist', related_name='items', on_delete=models.CASCADE, db_index=True)
    product = models.ForeignKey('Product', related_name='wishlist_items', on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.product.name} in Wishlist'
