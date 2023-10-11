from django.conf import settings
from django.contrib import admin
from rest_framework import routers
from django.urls import path, include
from django.conf.urls.static import static
from users.views import UserViewSet, GroupViewSet
from custom_menu.views import CategoryViewSet, ProductViewSet, FullCategoryViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"groups", GroupViewSet)
router.register(r"products", ProductViewSet, basename="products")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"full-categories", FullCategoryViewSet, basename="full-categories")

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("sandwich-api/", include("users.urls")),
    path("sandwich-api/", include("invoice.urls")),
    path("sandwich-api/", include("custom_menu.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
