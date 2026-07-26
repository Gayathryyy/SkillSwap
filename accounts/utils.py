import random
from django.core.mail import send_mail
from django.conf import settings


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(email, otp):

    subject = "SkillSwap Email Verification OTP"

    message = f"""
Hello,

Your SkillSwap verification OTP is:

{otp}

Please enter this OTP to complete your registration.

Thank you.
"""

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )