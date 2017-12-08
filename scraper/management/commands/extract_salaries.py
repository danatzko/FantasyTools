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
                
                # Salary has an odd format.  Needs to be cast as a float
                salary = float(0.0) if row['salary'] == '' else float(row['salary'])
                points = float(row['points'])
                points_for = points_against = points
                
                ## Setup object references

                # Each "stat" row represents a score for a player and a team.  
                # team  [away || home] [points_for]
                # oppt  [points_against] (future)
                if row['h_a'] == 'h':
                    home,home_created = Team.objects.get_or_create(name=row['team'])
                    away,away_created = Team.objects.get_or_create(name=row['oppt'])
                    team = home
                    if row['pos'] == 'Def':
                        home.d_points += points_for
                        home.d_points_home += points_for
                    else:
                        home.o_points += points_for
                        home.o_points_home += points_for
                else:
                    home,home_created = Team.objects.get_or_create(name=row['oppt'])
                    away,away_created = Team.objects.get_or_create(name=row['team'])
                    team = away
                    if row['pos'] == 'Def':
                        away.d_points += points_for
                        away.d_points_away += points_for
                    else:
                        away.o_points += points_for
                        away.o_points_away += points_for
                
                player,player_created = Player.objects.get_or_create(name=row['name'],pos=row['pos'],team=row['team'])
                player.points += points
                player.games += 1
                player.avg_points_game = player.points / player.games
                
                stat = GameStats(
                    Player_id=player.id,
                    Home=home,
                    Away=away,
                    salary=salary,
                    pos=row['pos'],
                    points=row['points'],
                    week=row['week'],
                    year=row['year'],
                )
                # Attempt to store the data to the DB.  Otherwise, stop the program
                # and print the offending row.
                try:
                    stat.save()
                    player.save()
                    home.save()
                    away.save()
                    #self.stdout.write(player.name)
                    #self.stdout.write(home.name)
                    #self.stdout.write(away.name)
                except ValueError:
                    print(row)
                    break