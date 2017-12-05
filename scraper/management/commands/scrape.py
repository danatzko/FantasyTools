from django.core.management.base import BaseCommand, CommandError
import execnet


class Command(BaseCommand):
    args = 'week'
    help = 'Initiates a Scrape session'

    def add_arguments(self, parser):
        parser.add_argument('week', nargs='+', type=int)
        parser.add_argument('year', nargs='+', type=int)
        parser.add_argument('threshold', nargs='+', type=int)

    def handle(self, *args, **options):
        year = options['year']
        week = options['week']
        threshold = options['threshold']

        gw = execnet.makegateway("popen//python=python2.7")
        
        channel = gw.remote_exec('''
            import nflgame
            channel.send(nflgame.combine_game_stats(nflgame.games({week}, {year})))
        '''.format(week=week,year=year))
        
        players = channel.receive()
        qbs = {}
        wrs = {}
        rbs = {}
        tes = {}
        
        for p in players:
            score = self.score_player(p)
            if score > threshold:
                #print p.guess_position,p.name,p.team,score,p.formatted_stats()
                if p.guess_position == 'QB':
                    qbs[p.name] = score
                if p.guess_position == 'WR':
                    wrs[p.name] = score
                if p.guess_position == 'RB':
                    rbs[p.name] = score
                if p.guess_position == 'TE':
                    tes[p.name] = score
        
        self.stdout.write('week {0}'.format(options['week']))

    def score_player(player):
        scoring = {
            # Passing
            'passing_yds' : lambda x : x*.04,
            'passing_tds' : lambda x : x*4,
            'passing_twoptm'  : lambda x : x*2,
            # Rushing
            'rushing_yds' : lambda x : x*.1,
            'rushing_tds' : lambda x : x*6,
            'kickret_tds' : lambda x : x*6,
            'rushing_twoptm' : lambda x : x*2,
            # Receiving
            'receiving_tds' : lambda x : x*6,
            'receiving_yds' : lambda x : x*.1,
            'receiving_rec' : lambda x : x*.5,
            'receiving_twoptm' : lambda x : x*2,
            # Kicker
            'kicking_fgm_yds' : lambda x : (5 if x >= 50 else (4 if x >= 40 else 3)),
            'kicking_xpmade' : lambda x : x*1,
            'kicking_xpmissed' : lambda x : x*-1,
            'kicking_fgmissed' : lambda x : x*-1,
            # Various
            'fumbles_lost' : lambda x : x*-2, 
            'passing_ints' : lambda x : x*-2,
        }
        score = 0
        for stat in player._stats:
            if stat in scoring:
                score += scoring[stat](getattr(player,stat))    
        return score
