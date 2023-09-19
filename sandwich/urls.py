from django.conf import settings
from django.contrib import admin
from rest_framework import routers
from django.urls import path, include
from django.conf.urls.static import static
from users.views import UserViewSet, GroupViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"groups", GroupViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
