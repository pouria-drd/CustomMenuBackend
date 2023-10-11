from django.contrib import admin
from invoice.models import PaymentType, Invoice, InvoiceProducts, InvoiceProductDetails


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


# @admin.register(PaymentType)
# class PaymentDetailAdmin(admin.ModelAdmin):
#     list_display = [
#         "id",
#         "name",
#     ]


# @admin.register(InvoiceProductDetails)
# class InvoiceDetailInline(admin.ModelAdmin):
#     list_display = [
#         "id",
#         "invoice_product",
#         "price",
#         "count",
#     ]

#     search_fields = [
#         "invoice_product",
#         "price",
#         "count",
#     ]

#     list_filter = [
#         "invoice_product",
#         "price",
#         "count",
#     ]


# class InvoiceDetailInline(admin.TabularInline):
#     model = InvoiceProducts
#     extra = 1


# class InvoiceAdmin(admin.ModelAdmin):
#     inlines = [InvoiceDetailInline]

#     list_display = [
#         "invoice_number",
#         "user",
#         "payment_type",
#         "created_at",
#         "updated_at",
#     ]

#     exclude = ("invoice_number",)

#     search_fields = [
#         "user",
#         "payment_type",
#     ]

#     list_filter = [
#         "created_at",
#         "updated_at",
#     ]


# admin.site.register(Invoice, InvoiceAdmin)
# admin.site.register(InvoiceDetail)
