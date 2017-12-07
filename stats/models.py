from django.db import models

# Create your models here.

class GameStats(models.Model):
    
    Player = models.ForeignKey('Player',
        on_delete=models.DO_NOTHING,
        null=False,
        default=None,
    )

    Home = models.ForeignKey('Team',
        on_delete=models.DO_NOTHING,
        null=False,
        default=None,
    )  
    Away = models.ForeignKey('Team',
        on_delete=models.DO_NOTHING,
        null=False,
        default=None,
        related_name="OpposingTeam"
    )
    week = models.IntegerField(default=0)
    year = models.IntegerField(default=0)
    pos = models.CharField(max_length=5)
    salary = models.FloatField(default=0)
    points = models.FloatField(default=0)

class Player(models.Model):
    name = models.CharField(max_length=50, unique=True)
    games = models.IntegerField(default=0)
    plays = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    avg_salary = models.IntegerField(default=0)
    avg_points_game = models.IntegerField(default=0)
    avg_points_away = models.IntegerField(default=0)
    avg_points_home = models.IntegerField(default=0)
    deviation = models.IntegerField(default=0)

class Team(models.Model):
    name = models.CharField(max_length=5, unique=True)
    o_points = models.IntegerField(default=0)
    d_points = models.IntegerField(default=0)
    o_points_away = models.IntegerField(default=0)
    o_points_home = models.IntegerField(default=0)
    d_points_away = models.IntegerField(default=0)
    d_points_home = models.IntegerField(default=0)
    a_deviation = models.IntegerField(default=0)
    h_deviation = models.IntegerField(default=0)
    