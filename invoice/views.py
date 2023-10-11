from invoice.models import *
from invoice.serializers import *
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import CreateAPIView, ListAPIView


# Create API --------------------------------------------------------------------
class TempInvoiceCreateView(CreateAPIView):
    """
    API endpoint that allows temporary invoice to be create.
    """

    @transaction.atomic
    def post(self, request):
        print(request.data)
