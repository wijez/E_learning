from django.core.mail import send_mail
from django.conf import settings


def send_verification_email(email, verify_code):
    subject = 'Verify Your Email'
    message = f'Your verification code is: {verify_code}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
