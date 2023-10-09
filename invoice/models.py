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
    description = models.TextField(max_length=100, blank=True)
    user = models.ForeignKey(User, related_name="invoices", on_delete=models.RESTRICT)
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


class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(
        Invoice, related_name="invoice_details", on_delete=models.RESTRICT
    )

    price = models.ForeignKey(
        Price, related_name="invoice_detail_price", on_delete=models.RESTRICT
    )

    count = models.IntegerField(default=1)

    def __str__(self):
        name = f"{self.invoice}"
        return name
