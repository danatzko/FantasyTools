from django.core.management.base import BaseCommand, CommandError
import execnet


class Command(BaseCommand):
    args = 'week'
    args = 'year'
    args = 'threshold'
    help = 'Initiates a Scrape session'
    
    def add_arguments(self, parser):
        parser.add_argument('year', nargs='+', type=int)
        parser.add_argument('week', nargs='+', type=int)
        parser.add_argument('threshold', nargs='+', type=int)

    def handle(self, *args, **options):
        # options
        year=options['year']
        week=options['week']
        threshold=options['threshold']
        # Create a new interpreter
        gw=execnet.makegateway("popen//python=python2.7")
        # Multiline varaible string which is executed as a python2.7 script in a separate shell
        cmd = '''
            import os
            my_file = os.path.join(os.path.expanduser("~"), "venv/nflgame/nflgame/bin/activate_this.py")
            execfile(my_file,dict(__file__=my_file))
            
            import nflgame
            
            def score_player(player):
                scoring = {
                    'passing_yds' : lambda x : x*.04,
                    'passing_tds' : lambda x : x*4,
                    'passing_twoptm'  : lambda x : x*2,
                    'rushing_yds' : lambda x : x*.1,
                    'rushing_tds' : lambda x : x*6,
                    'kickret_tds' : lambda x : x*6,
                    'rushing_twoptm' : lambda x : x*2,
                    'receiving_tds' : lambda x : x*6,
                    'receiving_yds' : lambda x : x*.1,
                    'receiving_rec' : lambda x : x*.5,
                    'receiving_twoptm' : lambda x : x*2,
                    'fumbles_lost' : lambda x : x*-2, 
                    'passing_ints' : lambda x : x*-2,
                }
                score = 0
                for stat in player.stats:
                    if stat in scoring:
                        score += scoring[stat](getattr(player,stat))    
                return score

            players=nflgame.combine_game_stats(nflgame.games(%(year)s,%(week)s))
            response = {}
            for p in players:
                for stat in p.stats:
                    resposnse[p.guess_position[p.name]] = stat
            channel.send(repr(response))
        ''' % {'year':year[0],'week':week[0],'threshold':threshold[0]}
        
        # Execture the string
        channel=gw.remote_exec(cmd)

        # Get the response
        players = channel.receive()
        
        # For now, just print
        # TODO - After stats.models are available, store the DB with results 
        self.stdout.write(players)

        # TODO - error handling, defaults, and post processing
        
