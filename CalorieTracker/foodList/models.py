from django.db import models
import datetime
# Create your models here.
class Record(models.Model):
    uname = models.CharField(max_length=200)
    fname = models.CharField(max_length=500)
    carbs = models.FloatField()
    protien = models.FloatField()
    fats = models.FloatField()
    calories = models.FloatField()
    units = models.CharField(max_length=200, default=None)
    weight = models.FloatField(default=None)
    quantity = models.FloatField(default=None)
    time = models.DateTimeField(default=None)
    def __str__(self):
        return self.fname
