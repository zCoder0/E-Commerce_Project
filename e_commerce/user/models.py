from django.db import models
from django.utils import timezone

class UserRegister(models.Model):
    user_mobile = models.CharField(max_length=15, unique=True)
    user_name = models.CharField(max_length=50)
    user_email = models.EmailField(max_length=100, unique=True)
    user_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user_name


class UserDetails(models.Model):
    user = models.OneToOneField(
        'UserRegister',  # self app, can also just use UserRegister directly
        on_delete=models.CASCADE,
        related_name="details"
    )
    address = models.CharField(max_length=255, blank=True, default="")
    city = models.CharField(max_length=100, blank=True, default="")
    state = models.CharField(max_length=100, blank=True, default="")
    zip_code = models.CharField(max_length=20, blank=True, default="")
    country = models.CharField(max_length=100, blank=True, default="")

    def __str__(self):
        return f"{self.user.user_name} Details"

class CartDetails(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('purchased', 'Purchased'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey('user.UserRegister', on_delete=models.CASCADE)  # string reference
    
    product = models.ForeignKey(
        'inventory.ProductDetails', 
        on_delete=models.CASCADE)
    
    quantity = models.IntegerField()
    added_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Cart {self.id} - {self.user.user_name}"



class OrderDetails(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        'UserRegister', 
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'inventory.ProductDetails',  # string reference to avoid circular import
        on_delete=models.CASCADE
    )
    cart = models.ForeignKey(
        'user.CartDetails', 
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")
    shipping_address = models.CharField(max_length=255)
    shipping_city = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255)
    shipping_country = models.CharField(max_length=255)
    shipping_zipcode = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=255)

    def __str__(self):
        return f"Order {self.id} - {self.user.user_name}"
