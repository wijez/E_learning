from django.db import models


class Certificates(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE)
    course_id = models.ForeignKey('Courses', on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Certificate for {self.user_id.name} - {self.course_id.title}"
