from django.db import models
from django.utils import timezone

class CategoryDetails(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.category_name


class SupplierDetails(models.Model):
    supplier_name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.supplier_name


class ProductDetails(models.Model):
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer = models.IntegerField(default=0)
    stock = models.IntegerField()
    category = models.ForeignKey(CategoryDetails, on_delete=models.SET_NULL, null=True, blank=True)
    supplier = models.ForeignKey(SupplierDetails, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.product_name


class ProductImages(models.Model):
    product = models.ForeignKey(ProductDetails, on_delete=models.CASCADE, related_name="images")
    image_url = models.CharField(max_length=255, default="default_image.png")
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Image for {self.product.product_name}"


class Reviews(models.Model):
    user = models.ForeignKey('user.UserRegister', on_delete=models.CASCADE)  # string reference
    product = models.ForeignKey(ProductDetails, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    review_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review by {self.user.user_name} - {self.product.product_name}"
