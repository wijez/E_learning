from rest_framework.exceptions import ValidationError

from E_learning.app.models import Users


def validate_username_or_email(value):
    """Validate and fetch user based on email or username."""
    try:
        if '@' in value:
            user = Users.objects.get(email=value)
        else:
            user = Users.objects.get(username=value)
    except Users.DoesNotExist:
        raise ValidationError("User with the provided username or email does not exist.")
    return user