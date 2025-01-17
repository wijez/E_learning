import os

from django.core.mail import send_mail
from django.conf import settings

from E_learning.app.contants import RoleEnum
from E_learning.app.models import Users
from E_learning.settings import DEFAULT_FROM_EMAIL


def send_verification_email(recipient_email, verification_code):
    """
    Gửi email xác thực đến người dùng.
    """
    subject = 'Verify Your Email'
    message = f'Your verification code is: {verification_code}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])


def send_email_to_admins_and_super_users(course):
    admins_and_super_users = Users.objects.filter(role__in=[RoleEnum.ADMIN.value, RoleEnum.SUPER_USER.value])
    email_list = [admin.email for admin in admins_and_super_users if admin.email]

    if not email_list:
        return

    send_mail(
        subject='Request for Course Edit Approval',
        message=f'Lecturer has requested to edit the course "{course.title}". Please review the request.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=email_list,
    )