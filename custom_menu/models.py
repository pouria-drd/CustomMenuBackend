import uuid
from django.db import models


class Category(models.Model):
    persian_name = models.CharField(max_length=256)
    english_name = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    category_image = models.ImageField(
        default="category_default.png", upload_to="images/categories/"
    )

    def __str__(self):
        return self.persian_name


class Product(models.Model):
    guid = models.CharField(max_length=256, unique=True, default=uuid.uuid4())
    persian_name = models.CharField(max_length=256)
    english_name = models.CharField(max_length=256)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    product_image = models.ImageField(
        default="product_default.png", upload_to="images/products/"
    )

    category = models.ForeignKey(Category, on_delete=models.RESTRICT)

    def __str__(self):
        return self.persian_name


class Price(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.RESTRICT, related_name="price"
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.price)


class Quantity(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.RESTRICT, related_name="quantity"
    )
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_by_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.quantity)
