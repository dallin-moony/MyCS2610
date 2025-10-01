from django.db import models
from datetime import timedelta

# Create your models here.
class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100)
    
    def time_spent(self):
        delta = timedelta()
        for timelog in self.timelog_set.all():
            delta += (timelog.end_time - timelog.start_time)
        return str(delta)

class TimeLog(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
