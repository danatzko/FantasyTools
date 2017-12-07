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
                # Salary has an odd format.  Needs to be cast as a float
                salary = float(0.0) if row['salary'] == '' else float(row['salary'])

                # Create all the objects that don't exist

                player,created3 = Player.objects.get_or_create(name=row['name'])
                player.points += float(row['points'])
                player.games += 1
                player.avg_points_game = player.points / player.games
                # Player averages should really be run as a second job.  Jupyter Notebook for demo purposes?
                # player.avg_salary won't be accurate until all of the game stats are complete


                # row['team'] indicates which team scored, 
                # row['h_a'] indicates venue of score and team's relationship to it
                if row['h_a'] == 'h':
                    home,created = Team.objects.get_or_create(name=row['team'])
                    away,created2 = Team.objects.get_or_create(name=row['oppt'])
                else:
                    home,created = Team.objects.get_or_create(name=row['oppt'])
                    away,created2 = Team.objects.get_or_create(name=row['team'])

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
                    #self.stdout.write(player.name)
                    #self.stdout.write(home.name)
                    #self.stdout.write(away.name)
                except ValueError:
                    print(row)
                    break