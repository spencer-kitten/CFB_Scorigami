# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 19:57:14 2021

@author: spenc
"""
import pandas as pd
import datetime as datetime
import cfbd as cfb
import tweepy
from CFBD_Access import *
from Twitter_Access import *
from Winner_Loser import*

# Twitter API
auth = tweepy.OAuthHandler(API, API_S)
auth.set_access_token(Access, Access_S)
api = tweepy.API(auth)

def score_test(home_team,home_points,away_team,away_points,scores_df):
    '''Update Status on Twitter for new game data'''
    
    victor = max(home_points,away_points)
    loser = min(home_points,away_points)
    
    # Import missing scores as matrix
    missing_scores = missing_data_builder()
    
    # Test if new score is in matrix. If not, print last time score has appeared. 
    if missing_scores[victor][loser] == missing_scores[0][0]:
        year, hteam, ateam = last_score(victor,loser,scores_df)
        status_string = ("Final Score %s %d - %s %d." % (home_team,home_points, away_team, away_points))
        status_string1 = (" This score has happend before, no Scorigami. The last time this score happened was %d where %s played %s." % (year, hteam, ateam))
        status_string = status_string + status_string1
        print(status_string)
        api.update_status(status_string)
    else:
        status_string = ("Final Score %s %d - %s %d." % (home_team, home_points, away_team, away_points))
        status_string1 = (" Scorigami! This score has not happend before!")
        status_string = status_string + status_string1
        print(status_string)
        api.update_status(status_string)
        
    return 

def last_score(home_points,away_points,scores_df):
    '''Retrives information of last time score appeared'''
    
    home_points = int(home_points)
    away_points = int(away_points)
        
    # Retrive data and sort by year
    scores_df = scores_df.sort_values(by= 'Year', ascending = False)
    
    for game in scores_df.index:
        h = scores_df.iloc[game]['Home']
        a = scores_df.iloc[game]['Away']
        if ((h == home_points) and (a == away_points)) or ((a == home_points) and (h == away_points)) :
            year = scores_df.loc[game]['Year']
            hteam = scores_df.loc[game]['Home_Team']
            ateam = scores_df.loc[game]['Away_Team']
            return year, hteam, ateam
    return 0000, 'ERROR', 'ERROR'
