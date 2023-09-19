#  import base64
from custom_menu.models import *
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    # category_image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "persian_name",
            "is_active",
            # "category_image",
        ]

    def get_category_image(self, obj):
        if obj.category_image:
            # with open(obj.category_image.path, "rb") as image_file:
            #     image_data = image_file.read()
            #     encoded_string = base64.b64encode(image_data)
            #     return "data:image/*;base64," + encoded_string.decode("utf-8")
            return obj.category_image.url
        else:
            return None


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = [
            "product",
            "price",
        ]


class QuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Quantity
        fields = [
            "product",
            "quantity",
        ]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    price = PriceSerializer()
    quantity = QuantitySerializer()
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "persian_name",
            "description",
            "max_amount",
            "has_tax",
            "is_active",
            "category",
            "price",
            "quantity",
            "product_image",
        ]

    def get_product_image(self, obj):
        if obj.product_image:
            # with open(obj.product_image.path, "rb") as image_file:
            #     image_data = image_file.read()
            #     encoded_string = base64.b64encode(image_data)
            #     return "data:image/*;base64," + encoded_string.decode("utf-8")
            return obj.product_image.url
        else:
            return None
