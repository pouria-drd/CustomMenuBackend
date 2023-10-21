from invoice.models import *
from rest_framework import serializers


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType

        fields = ["id", "name"]


class InvoiceSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    payment_type = PaymentTypeSerializer()

    class Meta:
        model = Invoice

        fields = [
            "id",
            "invoice_number",
            "user",
            "payment_type",
            "created_at",
        ]

    def get_user(self, obj):
        if obj.user:
            return obj.user.username
        return None


class InvoiceProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceProductDetails
        fields = [
            "invoice_product",
            "price",
            "count",
        ]


class InvoiceProductsSerializer(serializers.ModelSerializer):
    invoice_product_details = InvoiceProductDetailsSerializer(many=True)

    class Meta:
        model = InvoiceProducts
        fields = ["invoice", "title", "description", "count", "invoice_product_details"]


class InvoiceDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    payment_type = PaymentTypeSerializer()
    invoice_products = InvoiceProductsSerializer(many=True)

    class Meta:
        model = Invoice
        fields = [
            "id",
            "payment_type",
            "invoice_number",
            "user",
            "payment_type",
            "created_at",
            "invoice_products",
        ]

    def get_user(self, obj):
        if obj.user:
            return obj.user.username
        return None


# Temporary Invoice  ----------------------------------------------------------------------
class TempInvoiceSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = TempInvoice

        fields = ["id", "user", "created_at"]

    def get_user(self, obj):
        if obj.user:
            return obj.user.username
        return None


class TempInvoiceProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempInvoiceProducts

        fields = ["title", "description", "count"]


class TempInvoiceProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempInvoiceProductDetails

        fields = ["price", "count"]
