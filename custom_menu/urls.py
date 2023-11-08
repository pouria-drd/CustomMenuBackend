from django.urls import path
from custom_menu.views import *

urlpatterns = [
    # Full data
    path("full-category/", FullCategoryListView.as_view(), name="full-category"),
    # List view
    path("products/", ProductListView.as_view(), name="product-list"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path(
        "default-menu-products/",
        DefaultMenuProductListView.as_view(),
        name="default-menu-product-list",
    ),
    # Create view
    path("prices/create/", PriceCreateView.as_view(), name="price-create"),
    path("products/create/", ProductCreateView.as_view(), name="product-create"),
    path("quantities/create/", QuantityCreateView.as_view(), name="quantity-create"),
    path("categories/create/", CategoryCreateView.as_view(), name="category-create"),
    # Update view
    path("products/<int:pk>/", ProductUpdateView.as_view(), name="product-update"),
    path("categories/<int:pk>/", CategoryUpdateView.as_view(), name="category-update"),
]
