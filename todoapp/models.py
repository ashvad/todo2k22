from django.db import models

# Create your models here.

class Todos(models.Model):
    task_name=models.CharField(max_length=120)
    user=models.CharField(max_length=12)
    completed_status=models.BooleanField(default=False)

    def __str__(self):
        return self.task_name

