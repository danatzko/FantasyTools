from django.db import models

# Create your models here.

class GameStats(models.Model):
    week = models.IntegerField(default=0)
    year = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    pos = models.CharField(max_length=5)
    team = models.CharField(max_length=5)
    oppt = models.CharField(max_length=5)
    salary = models.FloatField(default=0)
    h_a = models.CharField(max_length=1)
    points = models.FloatField(default=0)
    