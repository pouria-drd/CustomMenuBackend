from django.urls import path
from custom_menu.views import (
    # List view
    CategoryListView,
    ProductListView,
    # Update view
    ProductUpdateView,
    CategoryUpdateView,
)

urlpatterns = [
    # List view
    path("products/", ProductListView.as_view(), name="product-list"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    # Update view
    path("products/<int:pk>/", ProductUpdateView.as_view(), name="product-update"),
    path("categories/<int:pk>/", CategoryUpdateView.as_view(), name="category-update"),
]
