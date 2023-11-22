from users.views import *
from django.urls import path

urlpatterns = [
    path("users/login/", LoginAPIView.as_view(), name="user-login"),
    path("users/logout/", LogoutView.as_view(), name="user-logout"),
    path(
        "users/request-login-code/",
        RequestLoginCodeView.as_view(),
        name="request-login-code",
    ),
    path(
        "users/confirm-login-code/",
        ConfirmLoginCodeView.as_view(),
        name="confirm-login-code",
    ),
]
