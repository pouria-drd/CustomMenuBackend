import re
from random import randint
from users.models import *
from datetime import datetime

max_tries = 2


def validate_phone_number(phone_number):
    pattern = r"^(\+98|0)?9\d{9}$"  # This pattern matches Iran phone numbers in the format +989123456789 or 09123456789
    if re.match(pattern, phone_number):
        return True
    else:
        return False


def get_or_create_login_code(phone_number):
    # request
    # user_agent = request.META.get("HTTP_USER_AGENT")
    # ip_address = request.META.get("REMOTE_ADDR")

    customer, status = CustomerUser.objects.get_or_create(phone_number=phone_number)

    customer_login_code, status = CustomerLoginCode.objects.get_or_create(
        customer=customer
    )

    if customer_login_code.failed_tries > max_tries:
        customer.is_active = False
        customer.save()

        return {
            "status": False,
            "message": "حساب کاربری شما مسدود شده است",
        }

    if customer_login_code.failed_tries > 0:
        time_diff = datetime.utcnow() - customer_login_code.updated_at.replace(
            tzinfo=None
        )

        time_to_wait = (
            40 + (20 * customer_login_code.failed_tries)
        ) - time_diff.total_seconds()

        if time_to_wait > 0:
            return {
                "status": False,
                "message": f"تا ارسال مجدد {time_to_wait}",
            }

    customer_login_code.failed_tries += 1
    code = randint(10000, 99999)
    customer_login_code.code = code

    customer_login_code.save()

    return {
        "status": True,
        "message": code,
    }
