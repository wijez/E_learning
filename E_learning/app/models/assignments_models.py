from django.db import models


class Assignments(models.Model):
    id = models.AutoField(primary_key=True)
    lesson_id = models.ForeignKey('Lessons', on_delete=models.CASCADE,  null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100)
