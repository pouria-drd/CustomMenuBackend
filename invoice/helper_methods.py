from rest_framework import status
from invoice.models import Invoice
from custom_menu.models import Product
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


def get_invoice_detail(pk):
    try:
        invoice = get_object_or_404(Invoice, id=pk)

        data = {
            "id": invoice.id,
            "invoice_number": invoice.invoice_number,
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

        return data

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
