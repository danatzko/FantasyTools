/anaconda3/envs/django/FantasyTools


Install steps
=============
conda install pip
conda install django


select name,
round(avg(points),0) as avg_pts,
round(avg(salary),0) as avg_salary,
round(avg(salary)/avg(points),0) as avg_pt_cost,
count(*) as games_played
from stats_gamestats
where year=2017 and pos = "te"
group by name
having avg_pts > 12 and count(*) > 11
order by avg_pts
DESC limit 30

Top 30 RBs (11 games or more)
select name, 
round(avg(points),0) as avg_pts, 
round(avg(salary),0) as avg_salary,  
round(avg(salary)/avg(points),0) as avg_pt_cost, 
count(*) as games_played, 
max(points) as best_game, 
round(max(points) - avg(points),0) as plus_error, 
round(avg(points) - min(points),0) as minus_error 
from stats_gamestats  
where year=2017 
and pos = "rb" 
group by name  
having best_game > 20 
and count(*) > 11  
order by avg_pts DESC 
limit 30;

Fantasy Point Ranking by team w/ average
select team,pos,oppt,
round(sum(points),0) as total_team_pts,
round(sum(points)/2,0) as avg_team_pts_game
from stats_gamestats 
where year=2017 and pos!="def" 
and week in (12,13)
group by team,pos,oppt
having total_team_pts > 40 or avg_team_pts_game > 20
order by team,oppt,total_team_pts DESC 

Top 30 Individual Point leaders over last 3 games
select team,name,pos,
round(avg(points),0) as avg_pts, 
round(avg(salary),0) as avg_salary,  
round(avg(salary)/avg(points),0) as avg_pt_cost, 
count(*) as games_played, 
max(points) as best_game, 
round(max(points) - avg(points),0) as plus_error, 
round(avg(points) - min(points),0) as minus_error 
from stats_gamestats  
where year=2017 
and week in (12,13)
group by name,team,pos
order by avg_pts DESC 
limit 30;


select team,name,pos,
round(avg(points),0) as avg_pts, 
round(avg(salary),0) as avg_salary,  
round(avg(salary)/avg(points),0) as avg_pt_cost, 
max(points) as best_game, 
round(max(points) - avg(points),0) as plus_error, 
round(avg(points) - min(points),0) as minus_error 
from stats_gamestats  
where year=2017 
and week in (12,13)
and pos='qb'
group by name,team,pos
order by avg_pts DESC 


select team,points,oppt
from stats_gamestats 
where pos = 'def' and year = 2017 and week = 13
order by points desc

select team,sum(points) as total_team_pts, count(*) 
from stats_gamestats 
where year = 2017 and week = 13
group by team,points


select *
from stats_gamestats 
where pos in ('wr','rb')
and year = 2017 
and week = 13
and points > 20
and salary < 4700
order by week

select team,sum(points),oppt
from stats_gamestats 
where oppt = 'jac' and pos='qb' and year = 2017
group by team,points
order by week