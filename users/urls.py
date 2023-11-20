from django.urls import path
from users.views import LoginAPIView, LogoutView, RequestLoginView

urlpatterns = [
    path("users/login/", LoginAPIView.as_view(), name="user-login"),
    path("users/logout/", LogoutView.as_view(), name="user-logout"),
    path(
        "users/request_customer_login/",
        RequestLoginView.as_view(),
        name="request-customer-login",
    ),
]
