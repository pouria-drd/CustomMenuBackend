from django.urls import path
from invoice.views import TempInvoiceCreateView

urlpatterns = [
    path("temp-invoice/", TempInvoiceCreateView.as_view(), name="temp-invoice"),
]
