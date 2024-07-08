import re
from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken


def get_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user_id": user.id,
        "email": user.email,
        "login_count": user.login_count,
    }


def is_valid_email(email):
    return re.match(settings.EMAIL, email) is not None


def send_mail_for_login_otp(data):
    email = EmailMessage(
        subject="Login password OTP",
        body=f"Your login password OTP is {data.get('otp')}.",
        from_email=settings.EMAIL_HOST_USER,
        to=[data.get("mail")],
    )
    email.send()
