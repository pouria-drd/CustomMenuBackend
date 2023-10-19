from invoice.models import *
from rest_framework import serializers


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType

        fields = ["id", "name"]


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
