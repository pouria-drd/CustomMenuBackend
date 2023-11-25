from django.conf import settings
from django.http import HttpResponse
from users.models import CustomerLoginSession
from django.utils.deprecation import MiddlewareMixin


class CustomTokenAuthenticationMiddleware(MiddlewareMixin):
    URLS = settings.CUSTOM_TOKEN_ALLOWED_URLS

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path in self.URLS:
            # Check for the presence of the custom token in the request headers
            if "X-Customer-Auth" not in request.headers:
                return HttpResponse("Token not provided.", status=401)

            # Extract the custom token from the headers
            custom_token = request.headers.get("X-Customer-Auth")

            # Validate the custom token against the CustomerLoginSession model
            try:
                user_agent = request.META.get("HTTP_USER_AGENT")
                ip_address = request.META.get("REMOTE_ADDR")

                session = CustomerLoginSession.objects.get(session_guid=custom_token)

                if (
                    session.client_ip != ip_address
                    or session.client_user_agent != user_agent
                ):
                    session.delete()
                    return HttpResponse("Unauthorized token.", status=401)

                # ToDo: expire by session.last_try

                # Attach the associated CustomerUser to the request
                request.customer = session.customer
                session.save()

            except CustomerLoginSession.DoesNotExist:
                return HttpResponse("Invalid session.", status=401)

            except:
                return HttpResponse("Token not valid.", status=400)
