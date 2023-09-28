from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from custom_menu.models import Category, Product
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from custom_menu.serializers import (
    CategorySerializer,
    ProductSerializer,
    FullCategorySerializer,
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
    # Query to retrieve all instances of Category model
    queryset = Category.objects.all()
    serializer_class = CategoryUpdateSerializer  # Serializer class for Category model
    permission_classes = [AllowAny]  # Allow any user to access this view
    http_method_names = ["post"]  # Only patches are allowed


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
