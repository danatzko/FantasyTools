from django.core.management.base import BaseCommand, CommandError
import csv
import os
from stats.models import GameStats

CSV_FILE = os.path.join(os.path.expanduser("~"), "Projects/dk_salaries_2017.csv")


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        with open(CSV_FILE, newline='') as csvfile:
            my_reader = csv.DictReader(csvfile)
            for row in my_reader:
                salary = row['salary']
                if salary == '':
                    salary = float(0.0)
                else:
                    salary = float(salary)

                stat = GameStats(
                    week=row['week'],
                    year=row['year'],
                    name=row['name'],
                    pos=row['pos'],
                    team=row['team'],
                    oppt=row['oppt'],
                    salary=salary,
                    points=row['points'],
                    h_a=row['h_a'],
                )
                try:
                    stat.save()
                except ValueError:
                    print(row)
                    break