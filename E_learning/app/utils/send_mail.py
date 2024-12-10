from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(recipient_email, verification_code):
    """
    Gửi email xác thực đến người dùng.
    """
    subject = 'Verify Your Email'
    message = f'Your verification code is: {verification_code}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])
