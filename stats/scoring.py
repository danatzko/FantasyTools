import argparse
import nflgame

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

def score_player(player):
    score = 0
    for stat in player._stats:
        if stat in scoring:
            score += scoring[stat](getattr(player,stat))    
    return score

def run():
    parser = argparse.ArgumentParser(
        description='Takes the passed week and gets fantasy score for players '
                    'based on interest.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    aa = parser.add_argument
    aa('--year', default=2017, type=int,
       help='Pick a year to get fantasy points for.')
    aa('--week', default=1, type=int,
       help='Pick a week to get fantasy points for.')
    aa('--threshold', default=20, type=int,
       help='Show players with scores greater than threshold.')
    args = parser.parse_args()

    year = args.year    
    week = args.week
    threshold = args.threshold

    players = nflgame.combine_game_stats(nflgame.games(year, week))
    qbs = {}
    wrs = {}
    rbs = {}
    tes = {}

    for p in players:
        score = score_player(p)
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

    print len(qbs)
    print qbs
    print len(wrs)
    print wrs
    print len(rbs)
    print rbs
    print len(tes)
    print tes

if __name__ == '__main__':
    run()