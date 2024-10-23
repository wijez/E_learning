from django.db import models

from E_learning.app.contants import StatusEnum


class Enrollments(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE)
    course_id = models.ForeignKey('Courses', on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=StatusEnum.choice(),
                              default=StatusEnum.IN_PROCESS.value)

    def __str__(self):
        return f"{self.course_id} - {self.enrolled_at} - {self.status}"
