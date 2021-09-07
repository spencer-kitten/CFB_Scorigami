# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 19:57:14 2021

@author: spenc
"""
import pandas as pd
import datetime as datetime
import cfbd as cfb
from CFBD_Access import *
from Twitter_Access import *

# Twitter API
auth = tweepy.OAuthHandler(API, API_S)
auth.set_access_token(Access, Access_S)
api = tweepy.API(auth)

def score_test(home_team,home_points,away_team,away_points):
    '''Update Status on Twitter for new game data'''
    
    # Import missing scores as matrix
    missing_scores = pd.read_csv('Missing_Scores.csv')
    
    # Test if new score is in matrix. If not, print last time score has appeared. 
    if missing_scores[home_points][away_points] != missing_scores[0][0]:
        year = last_score(home_points,away_points)
        status_string = ("Beep Boop. I'm a bot. Final Score %s %f - %s %f." % (home_team,home_points, away_team, away_points))
        status_string1 = (" This score has happend before, no Scorigami. The last time this score happened was %f" % (year))
        status_string = status_string + status_string1
        api.update_status(status_string)
    else:
        status_string = ("Beep Boop. I'm a bot. Final Score %s %f - %s %f." % (home_team, home_points, away_team, away_points))
        status_string1 = (" Scorigami! This score has not happend before!")
        api.update_status(status_string)
        
    return 

def last_score(home_points,away_points):
    '''Retrives information of last time score appeared'''
        
    # Retrive data and sort by year
    scores_df = pd.read_csv('CFB_scores.csv')
    scores_df = scores_df.sort_values(by= 'Year', ascending = False)
    
    for game in scores_df:
        if (game['Home'] == home_points) and (game['Away'] == away_points):
            return game['Year']
        
        
        
