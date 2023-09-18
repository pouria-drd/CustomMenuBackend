from users import views
from django.contrib import admin
from rest_framework import routers
from django.urls import include, path
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
