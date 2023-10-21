from datetime import date
from invoice.models import *
from custom_menu.models import *
from invoice.serializers import *
from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView


# List API ----------------------------------------------------------------------
class PaymentChoiceListView(ListAPIView):
    """
    API endpoint that allows payment choices to be viewed.
    """

    # Query to retrieve all instances of Category model
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer  # Serializer class for Category model
    permission_classes = [IsAdminUser]  # Allow any user to access this view


class InvoiceDetailAPIView(APIView):
    """
    API endpoint that allow a detailed invoice to be viewed.
    """

    permission_classes = [IsAdminUser]  # Allow any user to access this view

    def get(self, request, pk):
        try:
            invoice = get_object_or_404(Invoice, id=pk)

            data = {
                "id": invoice.id,
                "created_at": invoice.created_at,
                "description": invoice.description,
                "products": [],
            }

            username = f"{invoice.user}"

            if username:
                data["user"] = username

            invoice_total_price = 0

            for product in invoice.invoice_products.prefetch_related(
                "invoice_product_details__price__product"
            ):
                product_data = {
                    "title": product.title,
                    "description": product.description,
                    "count": product.count,
                    "details": [],
                }

                product_total_price = 0

                for detail in product.invoice_product_details.all():
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

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(
                {"message": "مشکلی پیش آمده است"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class InvoiceListView(ListAPIView):
    """
    API endpoint that allows invoice to be viewed.
    """

    # Query to retrieve all instances of Category model
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer  # Serializer class for Category model
    permission_classes = [IsAdminUser]  # Allow any user to access this view

    def get_queryset(self):
        queryset = Invoice.objects.all()
        start_date = self.request.query_params.get(
            "start_date", None
        )  # Get the start date from query parameters
        end_date = self.request.query_params.get(
            "end_date", None
        )  # Get the end date from query parameters

        if start_date and end_date:
            # Filter invoices between start_date and end_date
            queryset = queryset.filter(created_at__date__range=[start_date, end_date])
        else:
            # Filter invoices for today's date
            queryset = queryset.filter(created_at__date=date.today())

        return queryset


class TempInvoiceListView(ListAPIView):
    """
    API endpoint that allows temporary invoice to be viewed.
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
                "products": [],
            }

            username = f"{temp_invoice.user}"

            if username:
                data["user"] = username

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

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(
                {"message": "مشکلی پیش آمده است"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


def get_unique_product_total_count(temp_invoice_products_list: list):
    unique_product_list = {}

    for product in temp_invoice_products_list:
        for detail in product.temp_invoice_product_details.all():
            item = {
                "product_id": str(detail.price.product.id),
                "total_count": detail.count * product.count,
            }

            if item["product_id"] in unique_product_list:
                unique_product_list[str(detail.price.product.id)] += (
                    detail.count * product.count
                )
            else:
                unique_product_list[str(detail.price.product.id)] = (
                    detail.count * product.count
                )

    return unique_product_list


def check_for_quantity(unique_product_list: dict):
    for item in unique_product_list:
        product = get_object_or_404(Product, id=item)
        latest_quantity = int(str(product.quantities.order_by("-created_at").first()))

        if unique_product_list[item] > latest_quantity:
            return {"message": f"موجودی {product} کافی نیست", "status": False}

    return {"status": True, "message": "ok"}


# Create API --------------------------------------------------------------------
class InvoiceCreateView(CreateAPIView):
    """
    API endpoint that allows invoice to be create.
    """

    permission_classes = [IsAdminUser]  # Allow any user to access this view

    @transaction.atomic
    def post(self, request):
        user = request.user

        temp_invoice_id = request.data.get("temp_invoice_id")
        payment_type_id = request.data.get("payment_type_id")

        temp_invoice = get_object_or_404(TempInvoice, id=temp_invoice_id)

        temp_invoice_products_list = temp_invoice.temp_invoice_products.all()

        unique_product_dict = get_unique_product_total_count(temp_invoice_products_list)

        quantity_check = check_for_quantity(unique_product_dict)

        if not quantity_check["status"]:
            return Response(
                {"message": quantity_check["message"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment_type = get_object_or_404(PaymentType, id=payment_type_id)

        new_invoice = None

        if user:
            new_invoice = Invoice.objects.create(user=user, payment_type=payment_type)
        else:
            new_invoice = Invoice.objects.create(payment_type=payment_type)

        temp_invoice_products_list = temp_invoice.temp_invoice_products.all()

        for product in temp_invoice_products_list:
            new_product = InvoiceProducts.objects.create(
                invoice=new_invoice,
                count=product.count,
                title=f"{new_invoice} فاکتور",
                description=f"{product.count} عدد از این محصول",
            )

            for detail in product.temp_invoice_product_details.all():
                new_detail = InvoiceProductDetails.objects.create(
                    invoice_product=new_product, count=detail.count, price=detail.price
                )

        for item in unique_product_dict:
            product = get_object_or_404(Product, id=item)
            latest_quantity = int(
                str(product.quantities.order_by("-created_at").first())
            )

            new_quantity = latest_quantity - unique_product_dict[item]

            quantity = Quantity.objects.create(
                product=product, quantity=new_quantity, is_by_user=False
            )

        temp_invoice.delete()

        return Response({"data": "ok"}, status=status.HTTP_200_OK)


class TempInvoiceCreateView(CreateAPIView):
    """
    API endpoint that allows temporary invoice to be create.
    """

    permission_classes = [IsAdminUser]  # Allow any user to access this view

    @transaction.atomic
    def post(self, request):
        try:
            user = request.user

            if user:
                temp_invoice = TempInvoice.objects.create(user=user)
            else:
                temp_invoice = TempInvoice.objects.create()

            for index, data in enumerate(request.data):
                listCount = int(str(data["count"]))

                temp_invoice_product = TempInvoiceProducts.objects.create(
                    invoice=temp_invoice, count=listCount
                )

                for item in data["items"]:
                    item_count = item["count"]
                    productID = item["productID"]
                    product = Product.objects.get(id=productID)

                    latest_quantity = int(
                        str(product.quantities.order_by("-created_at").first())
                    )

                    total_count = listCount * item_count

                    if total_count > latest_quantity:
                        return Response(
                            {"message": "عدم موجودی", "code": 100},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    latest_price = product.prices.order_by("-created_at").first()

                    temp_invoice_product_detail = (
                        TempInvoiceProductDetails.objects.create(
                            invoice_product=temp_invoice_product,
                            price=latest_price,
                            count=item_count,
                        )
                    )

            return Response(
                {"message": "عملیات موفق بود"}, status=status.HTTP_201_CREATED
            )

        except:
            return Response(
                {"message": "مشکلی پیش آمده است"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
