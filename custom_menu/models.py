import uuid
from django.db import models
from django.utils.html import mark_safe


class Category(models.Model):
    persian_name = models.CharField(
        max_length=100,
    )

    english_name = models.CharField(
        max_length=100,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    category_image = models.ImageField(
        default="category_default.png", upload_to="images/categories/"
    )

    def __str__(self):
        return self.persian_name

    def img_preview(self):
        return mark_safe(f'<img src = "{self.category_image.url}" width = "50"/>')


class Product(models.Model):
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    persian_name = models.CharField(max_length=100)

    english_name = models.CharField(max_length=100)

    description = models.TextField(max_length=100, blank=True)

    max_amount = models.IntegerField(default=2)

    is_active = models.BooleanField(default=True)

    has_tax = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    product_image = models.ImageField(
        default="product_default.png", upload_to="images/products/"
    )

    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT, related_name="products"
    )

    def __str__(self):
        return self.persian_name

    def img_preview(self):
        return mark_safe(f'<img src = "{self.product_image.url}" width = "75"/>')


class Price(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.RESTRICT, related_name="prices"
    )

    price = models.IntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return str(self.price)


class Quantity(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.RESTRICT,
        related_name="quantities",
    )

    quantity = models.IntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    is_by_user = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.quantity)
