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
        year=options['year']
        week=options['week']
        threshold=options['threshold']
        gw=execnet.makegateway("popen//python=python2.7")
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
                    'kicking_fgm_yds' : lambda x : (5 if x >= 50 else (4 if x >= 40 else 3)),
                    'kicking_xpmade' : lambda x : x*1,
                    'kicking_xpmissed' : lambda x : x*-1,
                    'kicking_fgmissed' : lambda x : x*-1,
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
            qbs = {}
            wrs = {}
            rbs = {}
            tes = {}
            for p in players:
                score = score_player(p)
                if score > %(threshold)s:
                    if p.guess_position == 'QB':
                        qbs[p.name] = score
                    if p.guess_position == 'WR':
                        wrs[p.name] = score
                    if p.guess_position == 'RB':
                        rbs[p.name] = score
                    if p.guess_position == 'TE':
                        tes[p.name] = score
            response['qbs'] = qbs
            response['rbs'] = rbs
            response['wrs'] = wrs
            response['tes'] = tes
            channel.send(repr(response))
        ''' % {'year':year[0],'week':week[0],'threshold':threshold[0]}
        
        channel=gw.remote_exec(cmd)

        players = channel.receive()
        
        self.stdout.write(players)
        
