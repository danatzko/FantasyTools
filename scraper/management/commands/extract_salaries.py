from django.core.management.base import BaseCommand, CommandError
import csv
import os
from stats.models import GameStats,Player,Team
'''
    The purpose of this script is to collect the game-by-game point and salary totals for the 2017 season
    Where the objects don't exist, they will be created.
'''
CSV_FILE = os.path.join(os.path.expanduser("~"), "Projects/dk_salaries_2017.csv")

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        with open(CSV_FILE, newline='') as csvfile:
            my_reader = csv.DictReader(csvfile)
            for row in my_reader:
                ## Normalize incoming Data
                
                my_objects = self.setup_objects(row)
                
                ## Setup object references

                # Each "stat" row represents a score for a player and a team.  
                # team  [away || home] [points_for]
                # oppt  [points_against] (future)
                
                stat = GameStats(
                    Player=my_objects['player'],
                    Home=my_objects['home'],
                    Away=my_objects['away'],
                    salary=my_objects['salary'],
                    pos=row['pos'],
                    points=row['points'],
                    week=row['week'],
                    year=row['year'],
                )
                # Attempt to store the data to the DB.  Otherwise, stop the program
                # and print the offending row.
                try:
                    stat.save()
                except ValueError:
                    print(row)
                    break
    def setup_objects(self,row):
         # Salary has an odd format.  Needs to be cast as a float
        salary = float(0.0) if row['salary'] == '' else float(row['salary'])
        points = float(row['points'])
        player,player_created = Player.objects.get_or_create(name=row['name'],pos=row['pos'],team=row['team'])
        player.points += points
        player.games += 1
        player.avg_points_game = player.points / player.games
        player.salary_total += salary
        player.avg_salary = player.salary_total / player.games

        if row['h_a'] == 'h':
            home,home_created = Team.objects.get_or_create(name=row['team'])
            away,away_created = Team.objects.get_or_create(name=row['oppt'])
            player.games_home += 1
            player.points_home += points
            player.avg_points_home = player.points_home / player.games_home
            
            player.salary_total_home += salary
            player.avg_salary_home = player.salary_total_home / player.games_home
            if row['pos'] == 'Def':
                home.d_points += points
                home.d_points_home += points
            else:
                home.o_points += points
                home.o_points_home += points
        else:
            home,home_created = Team.objects.get_or_create(name=row['oppt'])
            away,away_created = Team.objects.get_or_create(name=row['team'])
            player.games_away += 1
            player.points_away += points
            player.avg_points_away = player.points_away / player.games_away
            
            player.salary_total_away += salary
            player.avg_salary_away = player.salary_total_away / player.games_away
            if row['pos'] == 'Def':
                away.d_points += points
                away.d_points_away += points
            else:
                away.o_points += points
                away.o_points_away += points
        try:
            player.save()
            home.save()
            away.save()
        except ValueError:
            print(row)
                
        my_objects = {}
        my_objects['home'] = home
        my_objects['away'] = away
        my_objects['player'] = player
        my_objects['salary'] = salary
        return my_objects

        
        