from django.contrib import admin
from .models import Category, Product, Price, Quantity


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "persian_name",
        "english_name",
        "is_active",
        "created_at",
        "updated_at",
    ]

    list_filter = [
        "is_active",
    ]

    search_fields = [
        "persian_name",
        "english_name",
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "persian_name",
        "english_name",
        "category",
        "is_active",
        "created_at",
        "updated_at",
    ]

    list_filter = [
        "is_active",
        "category",
    ]

    search_fields = [
        "persian_name",
        "english_name",
    ]

    autocomplete_fields = [
        "category",
    ]


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = [
        "product",
        "price",
        "created_at",
        "updated_at",
    ]

    list_editable = [
        "price",
    ]

    search_fields = [
        "product__persian_name",
        "product__english_name",
    ]

    autocomplete_fields = [
        "product",
    ]


@admin.register(Quantity)
class QuantityAdmin(admin.ModelAdmin):
    list_display = [
        "product",
        "quantity",
        "created_at",
        "updated_at",
    ]

    list_editable = [
        "quantity",
    ]

    search_fields = [
        "product__persian_name",
        "product__english_name",
    ]

    autocomplete_fields = [
        "product",
    ]
