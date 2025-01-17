from django.db import models
from django.db.models import CASCADE

from E_learning.app.contants.status_enum import ChoicesEnum


class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    description = models.TextField(null=True)
    price = models.IntegerField(null=True)
    user = models.ForeignKey("Users", on_delete=models.CASCADE,null=True)
    invited_lecturers = models.ManyToManyField("Users", related_name='invited_courses', blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=ChoicesEnum.choice(),
                              default=ChoicesEnum.DRAFT.value.lower())

    def __str__(self):
        return f"{self.title}"

    def request_approval(self):
        """ Khi lecturer yêu cầu phê duyệt, cập nhật trạng thái """
        self.status = ChoicesEnum.PENDING_APPROVAL.value.lower()
        self.is_public = False
        self.save()

    def approve(self):
        """ Khi admin/super_user phê duyệt, cập nhật trạng thái """
        self.is_public = True
        self.status = ChoicesEnum.APPROVED.value.lower()
        self.save()
