from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext as _
from loguru import logger

def sent_otp_email(email, otp):
    subject = _("Your OTP code for login")
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    context = {
        "otp": otp,
        "site_name": settings.SITE_NAME,
        "expiry_time": settings.OTP_EXPIRATION,
    }
    # Some email clients can’t or won’t render HTML emails properly 
    # (e.g., some older clients, or users who prefer plain text).
    html_email = render_to_string("emails/otp.html", context)
    plain_email = strip_tags(html_email)
    email = EmailMultiAlternatives(subject, plain_email, from_email, recipient_list)
    email.attach_alternative(html_email, "text/html")
    try:
        email.send()
        logger.info(f"OTP sent to {email}")
    except Exception as e:
        logger.error(f"Failed to sent OTP to {email}: Error: {e}")

def send_account_locked_email(user, email):
    subject = _("Your account has been locked")
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    context = {
        "user": user,
        "lockout_duration": int(settings.LOCKOUT_DURATION.total_seconds() // 60),
        "site_name": settings.SITE_NAME

    }
    # Some email clients can’t or won’t render HTML emails properly 
    # (e.g., some older clients, or users who prefer plain text).
    html_email = render_to_string("emails/account_locked.html", context)
    plain_email = strip_tags(html_email)
    email = EmailMultiAlternatives(subject, plain_email, from_email, recipient_list)
    email.attach_alternative(html_email, "text/html")
    try:
        email.send()
        logger.info(f"Account locked email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to sent account locked email to {email}: Error: {e}")