from invoice.models import *
from custom_menu.models import *
from invoice.serializers import *
from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import CreateAPIView, ListAPIView


# List API ----------------------------------------------------------------------
class TempInvoiceListView(ListAPIView):
    """
    API endpoint that allows temporary invoice to be view.
    """

    # Query to retrieve all instances of Category model
    queryset = TempInvoice.objects.all()
    serializer_class = TempInvoiceSerializer  # Serializer class for Category model
    permission_classes = [IsAdminUser]  # Allow any user to access this view


class TempInvoiceDetailView(APIView):
    permission_classes = [IsAdminUser]  # Allow any user to access this view

    def get(self, request, pk):
        try:
            temp_invoice = get_object_or_404(TempInvoice, id=pk)
            data = {
                "id": temp_invoice.id,
                "created_at": temp_invoice.created_at,
                "description": temp_invoice.description,
                "user": temp_invoice.user,
                "products": [],
            }

            invoice_total_price = 0

            for product in temp_invoice.temp_invoice_products.prefetch_related(
                "temp_invoice_product_details__price__product"
            ):
                product_data = {
                    "title": product.title,
                    "description": product.description,
                    "count": product.count,
                    "details": [],
                }

                product_total_price = 0

                for detail in product.temp_invoice_product_details.all():
                    detail_data = {
                        "name": str(detail.price.product),
                        "has_tax": detail.price.product.has_tax,
                        "price": str(detail.price),
                        "count": detail.count,
                    }

                    total_price = detail.count * int(str(detail.price))

                    if detail.price.product.has_tax:
                        total_price += round(total_price * 9 / 100)

                    product_total_price += total_price

                    detail_data["total_price"] = total_price

                    product_data["details"].append(detail_data)

                product_data["total_price"] = product_total_price * product.count

                data["products"].append(product_data)

                invoice_total_price += product_data["total_price"]

            data["total_price"] = invoice_total_price

            return Response({"data": data}, status=status.HTTP_200_OK)

        except:
            return Response(
                {"message": "مشکلی پیش آمده است"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# Create API --------------------------------------------------------------------
class TempInvoiceCreateView(CreateAPIView):
    """
    API endpoint that allows temporary invoice to be create.
    """

    @transaction.atomic
    def post(self, request):
        temp_invoice = TempInvoice.objects.create()

        for index, data in enumerate(request.data):
            print("----- list", index + 1, " -----")
            listCount = int(str(data["count"]))
            print("list count:", listCount, ": \n")

            temp_invoice_product = TempInvoiceProducts.objects.create(
                invoice=temp_invoice, count=listCount
            )

            for item in data["items"]:
                item_count = item["count"]
                productID = item["productID"]
                product = Product.objects.get(id=productID)

                print("Product ID:", productID)
                print("Product Name:", item["name"])
                print("Product Count:", item_count, "\n")

                latest_quantity = int(
                    str(product.quantities.order_by("-created_at").first())
                )
                print("latest_quantity:", latest_quantity)

                total_count = listCount * item_count
                print("total_count:", total_count)

                if total_count > latest_quantity:
                    return Response(
                        {"message": "عدم موجودی", "code": 100},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                latest_price = product.prices.order_by("-created_at").first()
                print("latest_price:", latest_price)

                total_product_price = int(str(latest_price)) * item_count
                print("total_price:", total_product_price)
                print("******")

                temp_invoice_product_detail = TempInvoiceProductDetails.objects.create(
                    invoice_product=temp_invoice_product,
                    price=latest_price,
                    count=item_count,
                )

        return Response("Success")
