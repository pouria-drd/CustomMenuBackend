from django.contrib import admin
from invoice.models import PaymentType, Invoice, InvoiceDetail


@admin.register(PaymentType)
class PaymentDetailAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]


@admin.register(InvoiceDetail)
class InvoiceDetailInline(admin.ModelAdmin):
    list_display = [
        "id",
        "invoice",
        "price",
        "count",
    ]

    search_fields = [
        "invoice",
        "price",
        "count",
    ]

    list_filter = [
        "invoice",
        "price",
        "count",
    ]


class InvoiceDetailInline(admin.TabularInline):
    model = InvoiceDetail
    extra = 1


class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceDetailInline]

    list_display = [
        "invoice_number",
        "user",
        "payment_type",
        "created_at",
        "updated_at",
    ]

    exclude = ("invoice_number",)

    search_fields = [
        "user",
        "payment_type",
    ]

    list_filter = [
        "created_at",
        "updated_at",
    ]


admin.site.register(Invoice, InvoiceAdmin)
# admin.site.register(InvoiceDetail)
