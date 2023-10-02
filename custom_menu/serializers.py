#  import base64
from rest_framework import serializers
from custom_menu.models import Product, Category, Price, Quantity


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price

        fields = ["product", "price"]


class QuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Quantity

        fields = ["product", "quantity"]


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field="persian_name")
    latest_price = serializers.SerializerMethodField()
    latest_quantity = serializers.SerializerMethodField()
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
            "latest_price",
            "latest_quantity",
            "product_image",
        ]

    def get_latest_price(self, obj):
        latest_price = obj.prices.order_by("-id").first()

        if latest_price:
            serializer = PriceSerializer(instance=latest_price)
            return serializer.data
        return None

    def get_latest_quantity(self, obj):
        latest_quantity = obj.quantities.order_by("-id").first()
        if latest_quantity:
            serializer = QuantitySerializer(instance=latest_quantity)
            return serializer.data
        return None

    def get_product_image(self, obj):
        if obj.product_image:
            return self.context["request"].build_absolute_uri(obj.product_image.url)
        return None


class FullCategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    category_image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "persian_name",
            "english_name",
            "is_active",
            "category_image",
            "products",
        ]

    def get_category_image(self, obj):
        if obj.category_image:
            return self.context["request"].build_absolute_uri(obj.category_image.url)
        return None


class CategorySerializer(serializers.ModelSerializer):
    category_image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "persian_name",
            "english_name",
            "is_active",
            "category_image",
        ]

    def get_category_image(self, obj):
        if obj.category_image:
            return self.context["request"].build_absolute_uri(obj.category_image.url)
        return None


class CategoryUpdateSerializer(serializers.ModelSerializer):
    persian_name = serializers.CharField(required=True, max_length=20)
    english_name = serializers.CharField(required=False, max_length=20)
    is_active = serializers.BooleanField(default=True)
    category_image = serializers.ImageField(required=False)

    class Meta:
        model = Category
        fields = ["persian_name", "english_name", "is_active", "category_image"]

    # def get_category_image(self, obj):
    #     if obj.category_image:
    #         # with open(obj.category_image.path, "rb") as image_file:
    #         #     image_data = image_file.read()
    #         #     encoded_string = base64.b64encode(image_data)
    #         #     return "data:image/*;base64," + encoded_string.decode("utf-8")
    #         return obj.category_image.url
    #     else:
    #         return None


class ProductUpdateSerializer(serializers.ModelSerializer):
    product_image = serializers.ImageField(required=False)

    class Meta:
        model = Product
        fields = [
            "persian_name",
            "description",
            "max_amount",
            "has_tax",
            "is_active",
            "product_image",
        ]


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "persian_name",
            "english_name",
            "description",
            "max_amount",
            "is_active",
            "has_tax",
            "product_image",
            "category",
        ]
