from invoice.models import *
from django.contrib import admin


class InvoiceProductDetailsInline(admin.TabularInline):
    model = InvoiceProductDetails
    extra = 1


class InvoiceProductsInline(admin.TabularInline):
    model = InvoiceProducts
    inlines = [InvoiceProductDetailsInline]
    extra = 1


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ["invoice_number", "user", "payment_type", "created_at"]
    exclude = [
        "invoice_number",
    ]
    inlines = [InvoiceProductsInline]


@admin.register(InvoiceProducts)
class InvoiceProductsAdmin(admin.ModelAdmin):
    list_display = ["title", "invoice", "count"]


@admin.register(InvoiceProductDetails)
class InvoiceProductDetailsAdmin(admin.ModelAdmin):
    list_display = ["invoice_product", "price", "count"]


# Temporary Invoice  ----------------------------------------------------------------------
class TempInvoiceProductDetailsInline(admin.TabularInline):
    model = TempInvoiceProductDetails
    extra = 1


class TempInvoiceProductsInline(admin.TabularInline):
    model = TempInvoiceProducts
    inlines = [TempInvoiceProductDetailsInline]
    extra = 1


@admin.register(TempInvoice)
class TempInvoiceAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created_at"]
    inlines = [TempInvoiceProductsInline]


@admin.register(TempInvoiceProducts)
class TempInvoiceProductsAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "invoice", "count"]


@admin.register(TempInvoiceProductDetails)
class TempInvoiceProductDetailsAdmin(admin.ModelAdmin):
    list_display = ["id", "invoice_product", "price", "count"]
