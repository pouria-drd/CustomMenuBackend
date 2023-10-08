from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import TokenAuthentication


class CustomTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.select_related("user").get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid token.")

        if not token.user.is_active:
            raise AuthenticationFailed("User inactive or deleted.")

        # Get the expiration time from settings.py
        expiration_time = getattr(
            settings, "TOKEN_EXPIRATION_TIME", 24
        )  # Default to 24 hours if not specified

        # Check if the token has expired
        if token.created < timezone.now() - timedelta(hours=expiration_time):
            token.delete()
            raise AuthenticationFailed("Token has expired.")

        return token.user, token
