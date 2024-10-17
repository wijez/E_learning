import uuid

from django.db import models
from E_learning.app.contants import RoleEnum


# Create your models here.
class Users(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='user_images')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(default=RoleEnum.USER.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.name} - {self.email} - {self.role}"
