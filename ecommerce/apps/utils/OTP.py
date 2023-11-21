import random
from  string import digits
from secrets import choice as secret_choice
from django.core.cache import cache
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response

def otp_generator(size: int = 6, char: str = digits) -> str:
    return "".join(secret_choice(char) for _ in range(size))

def get_client_ip(request) -> str:
    return (
        x_forwarded_for.split(",")[0]
        if (x_forwarded_for := request.META.get("HTTP_X_FORWARDED_FOR"))
        else request.META.get("REMOTE_ADDR")
    )


def send_otp(request, phone):
    otp = otp_generator()
    ip = get_client_ip(request)
    cache.set(f"{ip}-for-authentication", phone, settings.EXPIRY_TIME_OTP)
    cache.set(phone, otp, settings.EXPIRY_TIME_OTP)

    # TODO Here the otp code must later be sent to the user's phone number by SMS system.
    # But in debug mode we return the otp code.
   
    context = {
        "otp": f"{otp}",
    }
    return Response(
        context,
        status=status.HTTP_200_OK,
    )