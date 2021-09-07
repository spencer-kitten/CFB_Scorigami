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

# CFBD API
api_instance = cfb.GamesApi(cfb.ApiClient(configuration))
   
# Pull working data
scores_df = pd.read_csv('CFB_scores.csv')


if __name__ == "__main__":
    A = True
    
    scores = {'Home':[],
              'Away':[],
              'Year':[],
              'ID':[],
              'Home_Team': [],
              'Away_Team': []
              }
    while A:
        current_year = datetime.datetime.now().year
        games = api_instance.get_games(year = current_year)
        for game_scores in games:
            if game_scores.id not in scores_df['ID'].values:
                if (game_scores.home_points != None) and (game_scores.home_team != None):
                    # Add in missing values
                    scores['Home'].append(game_scores.home_points)
                    scores['Away'].append(game_scores.away_points)
                    scores['Year'].append(current_year)
                    scores['ID'].append(game_scores.id)
                    scores['Home_Team'].append(game_scores.home_team)
                    scores['Away_Team'].append(game_scores.away_team)
                    
                    # Update Twitter
                    score_test(game_scores.home_team,game_scores.home_points,game_scores.away_team,game_scores.away_points,scores_df)
        
             
                            
        A = False
    # Save updated data to the main csv, then reload data
    scores = pd.DataFrame(scores)
    scores_df = pd.concat([scores_df,scores], axis = 0)
    scores_df.drop_duplicates(keep = 'first', inplace = True)
    scores_df.to_csv('CFB_scores.csv',index=False)
    scores_df = pd.read_csv('CFB_scores.csv')
    
