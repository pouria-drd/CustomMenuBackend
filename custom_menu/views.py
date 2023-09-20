from rest_framework.viewsets import ModelViewSet
from custom_menu.models import Category, Product
from rest_framework.generics import ListAPIView, UpdateAPIView
from custom_menu.serializers import CategorySerializer, ProductSerializer
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated


# List API ----------------------------------------------------------------------
class ProductListView(ListAPIView):
    """
    This view lists all instances of the Product model.
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


# Update API --------------------------------------------------------------------
class CategoryUpdateView(UpdateAPIView):
    """
    API endpoint that allows categories to be patched or put.
    """

    queryset = (
        Category.objects.all()
    )  # Query to retrieve all instances of Category model
    serializer_class = CategorySerializer  # Serializer class for Category model
    permission_classes = [AllowAny]  # Allow any user to access this view
    http_method_names = ["patch"]  # Only patches are allowed


class ProductUpdateView(UpdateAPIView):
    """
    API endpoint that allows products to be patched or put.
    """

    queryset = Product.objects.all()  # Query to retrieve all instances of Product model
    serializer_class = ProductSerializer  # Serializer class for Product model
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


class ProductViewSet(ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """

    queryset = Product.objects.all()  # Query to retrieve all instances of Product model
    serializer_class = ProductSerializer  # Serializer class for Product model
    permission_classes = [AllowAny]  # Allow any user to access this view
