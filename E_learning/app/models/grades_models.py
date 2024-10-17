from django.db import models


class Grades(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE)
    assignment_id = models.ForeignKey('Assignments', on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    graded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.user_id.name} - {self.assignment_id} - {self.score} - {self.graded_at} "
