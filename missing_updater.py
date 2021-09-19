#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 14:43:36 2021

@author: spencerkitten
"""
import pandas as pd
import tweepy
import matplotlib.pyplot as plt
import numpy as np
import datetime as datetime
import time

from CFBD_Access import *
from Twitter_Access import *
from Scorigami_Tester_v1 import *
from new_scorigami import *
from missing_updater import *
    
def missing_updater():
    # Twitter API
    auth = tweepy.OAuthHandler(API, API_S)
    auth.set_access_token(Access, Access_S)
    api = tweepy.API(auth)
    
    # CFBD API
    api_instance = cfb.GamesApi(cfb.ApiClient(configuration))
    
    # Pull working data
    winner_df = pd.DataFrame()
    winner_df = pd.read_csv('Missing_Scores2.csv')
    current_year = datetime.datetime.now().year
    games = []
    games = api_instance.get_games(year = current_year)
    
    # Iterate over all games this year. If scores have been updated, append data to working df and save.
    for game_scores in games:
        if game_scores.id not in winner_df['ID'].values:
            if (game_scores.home_points != None) and (game_scores.home_team != None):
                # Add in missing values
                scores = {'ID':[],
                          'MAX': [],
                          'MIN': []
                          }
                maximum = max(game_scores.home_team,game_scores.away_team)
                minimum = min(game_scores.home_team,game_scores.away_team)
                
                scores['ID'].append(game_scores.id)
                scores['MAX'].append(maximum)
                scores['MIN'].append(minimum)

                # Save updated data to the main csv, then reload data
                scores = pd.DataFrame(scores)
                winner_df = pd.concat([winner_df,scores], axis = 0)
                winner_df.drop_duplicates(keep = 'first', inplace = True)
                winner_df['MAX'] = winner_df['MAX'].astype(int)
                winner_df['MIN'] = winner_df['MIN'].astype(int)
                winner_df.to_csv('Missing_Scores2.csv',index=False)
                
                
                
                
                
                
                
                
                
                
                
                    