from custom_menu.models import *
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from custom_menu.models import Category, Product
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from custom_menu.serializers import (
    PriceSerializer,
    QuantitySerializer,
    CategorySerializer,
    ProductSerializer,
    FullCategorySerializer,
    ProductCreateSerializer,
    ProductUpdateSerializer,
    CategoryUpdateSerializer,
)


# List API ----------------------------------------------------------------------
class CategoryListView(ListAPIView):
    """
    This view lists all instances of the Category model.
    """

    queryset = (
        Category.objects.all()
    )  # Query to retrieve all instances of Category model
    serializer_class = CategorySerializer  # Serializer class for Category model
    permission_classes = [AllowAny]  # Allow any user to access this view


class FullCategoryListView(ListAPIView):
    """
    This view lists all instances of the Category model.
    """

    queryset = (
        Category.objects.all()
    )  # Query to retrieve all instances of Category model
    serializer_class = FullCategorySerializer  # Serializer class for Category model
    permission_classes = [AllowAny]  # Allow any user to access this view


class ProductListView(ListAPIView):
    """
    This view lists all instances of the Product model.
    """

    queryset = Product.objects.all()  # Query to retrieve all instances of Product model
    serializer_class = ProductSerializer  # Serializer class for Product model
    permission_classes = [AllowAny]  # Allow any user to access this view


# Create API --------------------------------------------------------------------
class CategoryCreateView(CreateAPIView):
    """
    API endpoint that allows categories to be create.
    """

    # Query to retrieve all instances of Category model
    queryset = Category.objects.all()
    serializer_class = CategoryUpdateSerializer  # Serializer class for Category model
    permission_classes = [AllowAny]  # Allow any user to access this view
    http_method_names = ["post"]  # Only post are allowed


class ProductCreateView(CreateAPIView):
    """
    API endpoint that allows products to be create.
    """

    # Query to retrieve all instances of Product model
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer  # Serializer class for Category model
    permission_classes = [AllowAny]  # Allow any user to access this view
    http_method_names = ["post"]  # Only post are allowed

    @transaction.atomic
    def post(self, request):
        price_data = request.data.get("price")
        quantity_data = request.data.get("quantity")

        product_serializer = ProductCreateSerializer(data=request.data)

        if product_serializer.is_valid():
            product_data = product_serializer.validated_data

            new_product = Product.objects.create(**product_data)

            new_price = Price.objects.create(product=new_product, price=price_data)
            new_quantity = Quantity.objects.create(
                product=new_product, quantity=quantity_data, is_by_user=True
            )

            new_product.save()
            new_price.save()
            new_quantity.save()

            return Response("success", status=status.HTTP_201_CREATED)
        else:
            return Response(
                product_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class PriceCreateView(CreateAPIView):
    """
    API endpoint that allows prices to be create.
    """

    # Query to retrieve all instances of Prices model
    queryset = Price.objects.all()
    serializer_class = PriceSerializer  # Serializer class for Category model
    permission_classes = [AllowAny]  # Allow any user to access this view
    http_method_names = ["post"]  # Only post are allowed

    def post(self, request):
        with transaction.atomic():
            try:
                product_id = request.data.get("product_id")
                new_price = int(str(request.data.get("price")))

                product = Product.objects.get(id=product_id)
                old_price = int(str(product.prices.order_by("-created_at").first()))

                if old_price == new_price:
                    return Response(
                        {"detail": "قیمت جدید برابر با قیمت قبلی است"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    price = Price.objects.create(product=product, price=new_price)
                    price.save()
                    product.save()
                    return Response(
                        {"detail": "قیمت با موفقیت به روز شد"},
                        status=status.HTTP_201_CREATED,
                    )
            except:
                return Response(
                    {"detail": "مشکلی پیش آمده است"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )


class QuantityCreateView(CreateAPIView):
    """
    API endpoint that allows quantities to be create.
    """

    # Query to retrieve all instances of Quantities model
    queryset = Quantity.objects.all()
    serializer_class = QuantitySerializer  # Serializer class for Category model
    permission_classes = [AllowAny]  # Allow any user to access this view
    http_method_names = ["post"]  # Only post are allowed

    def post(self, request):
        with transaction.atomic():
            try:
                product_id = request.data.get("product_id")
                new_quantity = int(str(request.data.get("quantity")))

                product = Product.objects.get(id=product_id)

                quantity = Quantity.objects.create(
                    product=product, quantity=new_quantity, is_by_user=True
                )

                quantity.save()
                product.save()
                return Response(
                    {"detail": "مقدار با موفقیت به روز شد"},
                    status=status.HTTP_201_CREATED,
                )
            except:
                return Response(
                    {"detail": "مشکلی پیش آمده است"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )


# Update API --------------------------------------------------------------------
class CategoryUpdateView(UpdateAPIView):
    """
    API endpoint that allows categories to be patched or put.
    """

    # Query to retrieve all instances of Category model
    queryset = Category.objects.all()
    serializer_class = CategoryUpdateSerializer  # Serializer class for Category model
    permission_classes = [AllowAny]  # Allow any user to access this view
    http_method_names = ["patch"]  # Only patches are allowed


class ProductUpdateView(UpdateAPIView):
    """
    API endpoint that allows products to be patched or put.
    """

    queryset = Product.objects.all()  # Query to retrieve all instances of Product model
    serializer_class = ProductUpdateSerializer  # Serializer class for Product model
    permission_classes = [AllowAny]  # Allow any user to access this view
    http_method_names = ["patch"]  # Only patches are allowed


# View Sets ---------------------------------------------------------------------
class CategoryViewSet(ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """

    queryset = (
        Category.objects.all()
    )  # Query to retrieve all instances of Category model
    serializer_class = CategorySerializer  # Serializer class for Category model
    permission_classes = [AllowAny]  # Allow any user to access this view


class FullCategoryViewSet(ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """

    queryset = (
        Category.objects.all()
    )  # Query to retrieve all instances of Category model
    serializer_class = FullCategorySerializer  # Serializer class for Category model
    permission_classes = [AllowAny]  # Allow any user to access this view


class ProductViewSet(ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """

    queryset = Product.objects.all()  # Query to retrieve all instances of Product model
    serializer_class = ProductSerializer  # Serializer class for Product model
    permission_classes = [AllowAny]  # Allow any user to access this view
