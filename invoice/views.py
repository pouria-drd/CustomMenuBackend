from invoice.models import *
from custom_menu.models import *
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
