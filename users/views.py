from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.serializers import UserSerializer, GroupSerializer, LoginSerializer


class LogoutView(APIView):
    """
    API endpoint that allows users to logout.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(
                {"message": "خروج موفقیت آیز بود"}, status=status.HTTP_200_OK
            )

        except:
            return Response(
                {"message": "خطایی رخ داده است دوباره تلاش کنید"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LoginAPIView(APIView):
    """
    API endpoint that allows users to login.
    """

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                # We are retrieving the token for authenticated user.
                if Token.objects.filter(user=user).exists():
                    token = Token.objects.get(user=user)
                    response = {
                        "status": status.HTTP_200_OK,
                        "message": "ورود موفقیت آمیز بود",
                        "data": {"Token": token.key},
                    }
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    # Create a new token for the user.
                    token = Token.objects.create(user=user)
                    response = {
                        "status": status.HTTP_200_OK,
                        "message": "ورود موفقیت آمیز بود",
                        "data": {"Token": token.key},
                    }
                    return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "نام کاربری یا رمز عبور اشتباه است",
                }
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "خطایی رخ داده است دوباره تلاش کنید",
            "data": serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class GroupViewSet(ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]
