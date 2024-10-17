from django.db import models


class Assignments(models.Model):
    id = models.AutoField(primary_key=True)
    lession_id = models.ForeignKey('Lessions', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100)
