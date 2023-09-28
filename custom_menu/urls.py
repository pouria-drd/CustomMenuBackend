from django.urls import path
from custom_menu.views import (
    # List view
    CategoryListView,
    ProductListView,
    # Full data
    FullCategoryListView,
    # Create view
    CategoryCreateView,
    # Update view
    ProductUpdateView,
    CategoryUpdateView,
)

urlpatterns = [
    # Full data
    path("full-category/", FullCategoryListView.as_view(), name="full-category"),
    # List view
    path("products/", ProductListView.as_view(), name="product-list"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    # Create view
    path("categories/create/", CategoryCreateView.as_view(), name="category-create"),
    # Update view
    path("products/<int:pk>/", ProductUpdateView.as_view(), name="product-update"),
    path("categories/<int:pk>/", CategoryUpdateView.as_view(), name="category-update"),
]
