from django.db import models


class Lessions(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey('Courses', on_delete=models.CASCADE, related_name='lessions')
    title = models.CharField(max_length=200)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
