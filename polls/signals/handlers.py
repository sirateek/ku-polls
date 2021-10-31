"""This file contain the signal listener for the authentication"""
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
import logging

logging = logging.getLogger(__name__)


def get_client_ip(request):
    """Get the visitor’s IP address using request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in)
def on_logged_in(sender, user, request, **kwargs):
    logging.info(f"{user} is logged in from {get_client_ip(request)}.")


@receiver(user_logged_out)
def on_logged_out(sender, user, request, **kwargs):
    logging.info(f"{user} is logged out from {get_client_ip(request)}.")


@receiver(user_login_failed)
def on_login_failed(sender, credentials, request, **kwargs):
    logging.warn(
        f"A login attempt for user `{credentials.get('username')}` from {get_client_ip(request)} was declined.")
