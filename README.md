# FantasyTools
DK Salary and Player Performance Corelations

Summary:
  Draft Kings fantasy sports publishes weekly tournaments where a tournament entry consist of a variety of skill positions 
  and a defense that acquire points throughout a football game.  Each player occupying a skill position has an associated salary.  
  In order for a Tournament Entry to be considered valid, the salary for all players on the entry is totaled and must be under $55k.  
  The highest point scoring entry wins.  Salaries typically increase/decrease as the player's performance changes

Goal:
  Determine if there is a relationship to a player's current DKsalary and future performance.

Approach:
 - Calculate Standard deviation for every QB, WR, RB, and TE and create a scoring algorithm for volatility
 - Establish a player rating system by comparing points/$, points/play, consecutive_starts and %_of_overall_team_production
 - Using volatility score, determine if any other factors present in the data will improve prediction accuracy of volatility swings

Assumptions:
 - Only 2014-2017 NFL Regular Season Stats will be calculated
 - Weather & Injuries will not be considered
 - Only Analyzing fantasy_pts_scored and opponent_fantasy_pts_scored
 - Defense is a single player
 - no kickers

Future:
 - Packaging
 - Testing
 - Deployment Instructions

Dependencies:
 nflgame - https://github.com/BurntSushi/nflgame for play-by-play statistics (nfl.com proxy)
 screen scraped data from http://rotoguru.net/ for Draft King Salaries

Disclaimer:
  This project is purely for my own education and demonstration purposes.  This software carries no guarantees whatsoever.
