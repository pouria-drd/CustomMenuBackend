from invoice.models import *
from rest_framework import serializers


class TempInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempInvoice

        fields = ["id", "user", "created_at"]


class TempInvoiceProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempInvoiceProducts

        fields = ["title", "description", "count"]


class TempInvoiceProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempInvoiceProductDetails

        fields = ["price", "count"]
