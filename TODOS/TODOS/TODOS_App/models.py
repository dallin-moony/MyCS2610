from django.db import models

# Create your models here.
class Todo(models.Model):
    id = models.BigAutoField(primary_key=True)
    contents = models.TextField()
    is_completed = models.BooleanField(default=False)

    