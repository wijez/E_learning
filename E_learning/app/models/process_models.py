from django.db import models


class Process(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE)
    course_id = models.ForeignKey('Courses', on_delete=models.CASCADE)
    lession_id = models.ForeignKey('Lessions', on_delete=models.CASCADE)
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user_id.name} - {self.course_id.title} - {self.progress_percentage}%"
