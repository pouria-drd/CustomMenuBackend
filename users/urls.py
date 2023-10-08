from django.urls import path
from users.views import LoginAPIView, LogoutView

urlpatterns = [
    path("users/login/", LoginAPIView.as_view(), name="user-login"),
    path("users/logout/", LogoutView.as_view(), name="user-logout"),
]
