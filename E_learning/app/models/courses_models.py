from django.db import models
from django.db.models import CASCADE


class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    description = models.TextField(null=True)
    price = models.IntegerField(null=True)
    user_id = models.ForeignKey("Users", on_delete=models.CASCADE,null=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
