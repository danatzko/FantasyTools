from django.db import models

'''
    FantastyTools.models

    From the game_stats CSV file, extrapolate a model indicative of performance
    over time given several scenarios:

    1.  Home vs Away
    2.  Point Distribution by Team (offense and defense)
    3.  Influencers and Magnifiers 
'''

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
    class Meta:
        unique_together = ('team','name','pos')    
    team = models.CharField(max_length=5, default=None)
    name = models.CharField(max_length=50)
    pos = models.CharField(max_length=5, default=None)
    games = models.IntegerField(default=0)
    games_away = models.IntegerField(default=0)
    games_home = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    points_home = models.IntegerField(default=0)
    points_away = models.IntegerField(default=0)
    salary_total = models.IntegerField(default=0)
    salary_total_home = models.IntegerField(default=0)
    salary_total_away = models.IntegerField(default=0)
    avg_salary = models.IntegerField(default=0)
    avg_salary_home = models.IntegerField(default=0)
    avg_salary_away = models.IntegerField(default=0)
    avg_points_game = models.IntegerField(default=0)
    avg_points_away = models.IntegerField(default=0)
    avg_points_home = models.IntegerField(default=0)


class Team(models.Model):
    name = models.CharField(max_length=5)
    o_points = models.IntegerField(default=0)
    d_points = models.IntegerField(default=0)
    o_points_away = models.IntegerField(default=0)
    o_points_home = models.IntegerField(default=0)
    d_points_away = models.IntegerField(default=0)
    d_points_home = models.IntegerField(default=0)    