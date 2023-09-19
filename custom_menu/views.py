from custom_menu.models import Category, Product
from rest_framework.generics import ListAPIView, RetrieveAPIView
from custom_menu.serializers import CategorySerializer, ProductSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser


class ProductListView(ListAPIView):
    """
    This view lists all instances of the Product model.
    """

    queryset = Product.objects.all()  # Query to retrieve all instances of Product model
    serializer_class = ProductSerializer  # Serializer class for Product model
    permission_classes = [AllowAny]  # Allow any user to access this view


class ProductDetailView(RetrieveAPIView):
    """
    This view retrieves a single instance of the Product model by its primary key.
    """

    queryset = Product.objects.all()  # Query to retrieve all instances of Product model
    serializer_class = ProductSerializer  # Serializer class for Product model
    permission_classes = [AllowAny]  # Allow any user to access this view


class CategoryListView(ListAPIView):
    """
    This view lists all instances of the Category model.
    """

    queryset = (
        Category.objects.all()
    )  # Query to retrieve all instances of Category model
    serializer_class = CategorySerializer  # Serializer class for Category model
    permission_classes = [AllowAny]  # Allow any user to access this view


class CategoryDetailView(RetrieveAPIView):
    """
    This view retrieves a single instance of the Category model by its primary key.
    """

    queryset = (
        Category.objects.all()
    )  # Query to retrieve all instances of Category model
    serializer_class = CategorySerializer  # Serializer class for Category model
    permission_classes = [AllowAny]  # Allow any user to access this view
