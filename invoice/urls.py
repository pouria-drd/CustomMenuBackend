from invoice.views import *
from django.urls import path

urlpatterns = [
    # POST ---------------------------------------------------------------------
    path("create-invoice/", InvoiceCreateView.as_view(), name="create-invoice"),
    path(
        "create-temp-invoice/",
        TempInvoiceCreateView.as_view(),
        name="create-temp-invoice",
    ),
    # GET ----------------------------------------------------------------------
    path("payment-choices/", PaymentChoiceListView.as_view(), name="payment-choices"),
    # main invoice
    path("invoice-list/", InvoiceListView.as_view(), name="invoice-list"),
    path("invoices/<int:pk>/", InvoiceDetailAPIView.as_view(), name="invoice-detail"),
    # temp invoice
    path("temp-invoice-list/", TempInvoiceListView.as_view(), name="temp-invoice-list"),
    path(
        "temp-invoice-detail/<int:pk>",
        TempInvoiceDetailView.as_view(),
        name="temp-invoice-detail",
    ),
]
