from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission, Group
from E_learning.app.contants import RoleEnum
from E_learning.app.utils import generate_verification_code


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    email = models.EmailField(unique=True)
    verify_code = models.CharField(max_length=6, blank=True)

    # Add role with choices from RoleEnum
    role = models.CharField(
        max_length=20,
        choices=RoleEnum.choice(),
        default=RoleEnum.USER.value  # Default is "USER"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Required fields for AbstractBaseUser
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',  # Changed name to avoid clash
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # Changed name to avoid clash
        blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.verify_code:  # Chỉ tạo mã nếu verify_code chưa tồn tại
            self.verify_code = generate_verification_code(6)
        super().save(*args, **kwargs)
