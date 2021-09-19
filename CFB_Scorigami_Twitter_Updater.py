# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 18:58:09 2021

@author: spenc
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

# CFBD API
api_instance = cfb.GamesApi(cfb.ApiClient(configuration))
   
# Load Hashtags
hashtags = pd.read_csv('Hashtags.csv')

# Create list to store weekly scorigamis 
weekly_scorigami = {'ID':[],
                    'MAX': [],
                    'MIN': []
                    }

if __name__ == "__main__":
    RUN = True
    new_score = True
    update_missing = True
    count = 0
    
    while RUN:
        
        # Pull working data
        scores_df = pd.DataFrame()
        scores_df = pd.read_csv('CFB_scores.csv')
        current_year = datetime.datetime.now().year
        games = []
        games = api_instance.get_games(year = current_year)
        
        # Iterate over all games this year. If scores have been updated, append data to working df and save.
        for game_scores in games:
            if game_scores.id not in scores_df['ID'].values:
                if (game_scores.home_points != None) and (game_scores.home_team != None):
                    # Add in missing values
                    scores = {'Home':[],
                              'Away':[],
                              'Year':[],
                              'ID':[],
                              'Home_Team': [],
                              'Away_Team': []
                              }
                    scores['Home'].append(game_scores.home_points)
                    scores['Away'].append(game_scores.away_points)
                    scores['Year'].append(current_year)
                    scores['ID'].append(game_scores.id)
                    scores['Home_Team'].append(game_scores.home_team)
                    scores['Away_Team'].append(game_scores.away_team)
                    
                    # Update Twitter & store scorigami
                    working_scorigami_store = score_test(game_scores.home_team,game_scores.home_points,game_scores.away_team,game_scores.away_points,scores_df, hashtags)
                    weekly_scorigami['ID'].append(game_scores.id)
                    weekly_scorigami['MAX'].append(max(game_scores.home_points,game_scores.away_points))
                    weekly_scorigami['MIN'].append(min(game_scores.home_points,game_scores.away_points))
                    
                    # Update Missing Scores
                    missing_updater()
                    
                    # Save updated data to the main csv, then reload data
                    scores = pd.DataFrame(scores)
                    scores_df = pd.concat([scores_df,scores], axis = 0)
                    scores_df.drop_duplicates(keep = 'first', inplace = True)
                    scores_df.to_csv('CFB_scores.csv',index=False)
                    
                    scores_df = pd.DataFrame()
                    scores_df = pd.read_csv('CFB_scores.csv')
                    
        # Cycle Count printed for user verification program is running.
        count += 1
        day = datetime.datetime.today().weekday()
        
        # 0 is Monday...
        if (day == 0) and (new == True):
            new_scorigami(weekly_scorigami)
            new_score = False
            update_missing = True
        elif (day == 1) and (update_missing = True):
            weekly_scorigami = {'ID':[],
                                'MAX': [],
                                'MIN': []
                                }
            new_score = True
            update_missing = False
        
        
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        second = datetime.datetime.now().second
        
        print('Cycle %d, Time: %d:%d:%d' % (count, hour,minute,second))
        time.sleep(60*1)
        
        
        
        
        
        
        
        
        
        