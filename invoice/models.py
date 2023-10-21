import datetime
from django.db import models
from custom_menu.models import Price
from django.contrib.auth.models import User


class PaymentType(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    invoice_number = models.PositiveIntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=255, blank=True)
    user = models.ForeignKey(
        User, blank=True, null=True, related_name="invoices", on_delete=models.RESTRICT
    )
    payment_type = models.ForeignKey(
        PaymentType, related_name="invoices", on_delete=models.RESTRICT
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            today = datetime.date.today()
            latest_invoice = (
                Invoice.objects.filter(created_at__date=today)
                .order_by("-invoice_number")
                .first()
            )
            if latest_invoice:
                self.invoice_number = latest_invoice.invoice_number + 1
            else:
                self.invoice_number = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice_number}"


class InvoiceProducts(models.Model):
    invoice = models.ForeignKey(
        Invoice, related_name="invoice_products", on_delete=models.RESTRICT
    )

    title = models.CharField(max_length=100, blank=True)

    description = models.TextField(max_length=255, blank=True)

    count = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class InvoiceProductDetails(models.Model):
    invoice_product = models.ForeignKey(
        InvoiceProducts,
        related_name="invoice_product_details",
        on_delete=models.RESTRICT,
    )

    price = models.ForeignKey(
        Price, related_name="invoice_product_detail_price", on_delete=models.RESTRICT
    )

    count = models.IntegerField(default=1)

    def __str__(self):
        name = f"{self.invoice_product}"
        return name


# Temporary Invoice  ----------------------------------------------------------------------
class TempInvoice(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=255, blank=True)
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name="temp_invoices",
        on_delete=models.RESTRICT,
    )

    def __str__(self):
        return f"{self.user} | invoice"


class TempInvoiceProducts(models.Model):
    invoice = models.ForeignKey(
        TempInvoice, related_name="temp_invoice_products", on_delete=models.CASCADE
    )

    title = models.CharField(max_length=100, blank=True)

    description = models.TextField(max_length=255, blank=True)

    count = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class TempInvoiceProductDetails(models.Model):
    invoice_product = models.ForeignKey(
        TempInvoiceProducts,
        related_name="temp_invoice_product_details",
        on_delete=models.CASCADE,
    )

    price = models.ForeignKey(
        Price,
        related_name="temp_invoice_product_detail_price",
        on_delete=models.RESTRICT,
    )

    count = models.IntegerField(default=1)

    def __str__(self):
        name = f"{self.invoice_product}"
        return name
