from django.db import models

# Create your models here.
class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100)

class TimeLog(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
