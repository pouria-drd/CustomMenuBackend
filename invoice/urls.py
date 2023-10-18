from invoice.views import *
from django.urls import path

urlpatterns = [
    path("temp-invoice/", TempInvoiceCreateView.as_view(), name="temp-invoice"),
    path("temp-invoice-list/", TempInvoiceListView.as_view(), name="temp-invoice-list"),
    path(
        "temp-invoice-list/<int:pk>",
        TempInvoiceDetailView.as_view(),
        name="temp-invoice-list",
    ),
]
