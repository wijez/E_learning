from django.db import models

from E_learning.app.contants import StatusEnum


class Process(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE, null=True)
    course_id = models.ForeignKey('Courses', on_delete=models.CASCADE, null=True)
    lesson_id = models.ForeignKey('Lessons', on_delete=models.CASCADE, null=True)
    last_accessed = models.DateTimeField(auto_now_add=True,null=True)
    status = models.CharField(choices=StatusEnum.choice(),
                              default=StatusEnum.IN_PROCESS.value)

    def __str__(self):
        return f"{self.user_id.name} - {self.course_id.title} - {self.last_accessed}"
