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

def score_test(home_team,home_points,away_team,away_points,scores_df, hashtags):
    '''Update Status on Twitter for new game data'''
    
    # Save twitter @ and hashtag information for use in tweet
    try:
        home_hash = hashtags[hashtags['Team'] == home_team]['HASH'].sum()
        #home_at = hashtags[hashtags['Team'] == home_team]['AT'].sum()
    except:
        home_hash = 'ERROR'
        #home_at = 'ERROR'
        
    try:
        away_hash = hashtags[hashtags['Team'] == away_team]['HASH'].sum()
        #away_at = hashtags[hashtags['Team'] == away_team]['AT'].sum()
    except:
        away_hash = 'ERROR'
        #away_at = 'ERROR'
    
    # Reassign scores to victor and loser team vice home and away
    victor = max(home_points,away_points)
    loser = min(home_points,away_points)
    
    # Import missing scores as matrix
    missing_scores = missing_data_builder()
    
    # Test if new score is in matrix. If not, print last time score has appeared. Print hashtags. Tweet all info.
    if missing_scores[victor][loser] == missing_scores[0][0]:
        year, hteam, ateam = last_score(victor,loser,scores_df)
        status_string = ("Final Score %s %d - %s %d.\n" % (home_team,home_points, away_team, away_points))
        status_string1 = ("No Scorigami.\nThe last time this score happened was %d where %s played %s.\n" % (year, hteam, ateam))
        status_string2 = ('%s %s' % (home_hash, away_hash))
        status_string = status_string + status_string1 + status_string2
        print(status_string)
        api.update_status(status_string)
        return (victor,loser)
    else:
        status_string = ("Final Score %s %d - %s %d.\n" % (home_team, home_points, away_team, away_points))
        status_string1 = ("SCORIGAMI!!!!\n")
        status_string2 = ('%s %s' % (home_hash, away_hash))
        status_string = status_string + status_string1 + status_string2
        print(status_string)
        api.update_status(status_string)
        
    return 

def last_score(home_points,away_points,scores_df):
    '''Retrives information of last time score appeared'''
    
    # Ensure types are correct
    home_points = int(home_points)
    away_points = int(away_points)
        
    # Retrive data and sort by year
    scores_df = scores_df.sort_values(by= 'Year', ascending = False)
    
    # Iterate over sorted years (going back in time from now) until first match is found
    for game in scores_df.index:
        h = scores_df.loc[game]['Home']
        a = scores_df.loc[game]['Away']
        if ((h == home_points) and (a == away_points)) or ((a == home_points) and (h == away_points)) :
            year = scores_df.loc[game]['Year']
            hteam = scores_df.loc[game]['Home_Team']
            ateam = scores_df.loc[game]['Away_Team']
            return year, hteam, ateam
    return 0000, 'ERROR', 'ERROR'
