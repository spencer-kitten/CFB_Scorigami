# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 09:36:05 2021

@author: spenc
"""

import cfbd as cfb
import pandas as pd
import tweepy
import matplotlib.pyplot as plt
import numpy as np
import datetime as datetime
import time

## CFB data
configuration = cfb.Configuration()
configuration.api_key['Authorization'] = 'yEoefkv11Eht+CxNyyu9PSwrgkBxkvldo1nUcuWT9FMz7FmG3skufO3dXTZ17jGq'
configuration.api_key_prefix['Authorization'] = 'Bearer'
api_instance = cfb.GamesApi(cfb.ApiClient(configuration))
   
# Twitter
API = 'DFR53M3XnPn3WYiG0mrFffNsb'
API_S = 'NYR4hId3mapginbIT0fmHPwuhK6FgV0IMuiIPgb3OK27oyH2lL'
Bearer = 'AAAAAAAAAAAAAAAAAAAAAFHETQEAAAAAq2D4yUNcGA88FiRqBLZ8Wx1SuZM%3D4xW8URRM4RNmG2l2gFrCorFpqcUAXNQiNEQf29enmw2E3ziXIU'
Access = '1434935301835616257-78mCvODyifUG7vKkmGg9l5TFSJ14j9'
Access_S = '8sZuaOHn74WAN4vK1ezbnt3f14zHq7BfRlw7Y9floi6XY'

auth = tweepy.OAuthHandler(API, API_S)
auth.set_access_token(Access, Access_S)
api = tweepy.API(auth)

# scores = {'Home':[],
#           'Away':[],
#           'Year':[],
#           'ID':[]
#           }
# years = range(1869,2021)
# for working_year in years:
#     games = api_instance.get_games(year = working_year)
#     for game_scores in games:
#         scores['Home'].append(round(game_scores.home_points))
#         scores['Away'].append(round(game_scores.away_points))
#         scores['Year'].append(int(working_year))
#         scores['ID'].append(game_scores.id)
        
# scores_df = pd.DataFrame(scores)
# scores_df.to_csv('CFB_scores.csv',index=False)

scores_df = pd.read_csv('CFB_scores.csv')

# Shows all time frequency of cfb scores
# nrows = scores_df['Home'].max() + 1
# nrows = int(nrows)
# ncols = scores_df['Away'].max() + 1
# ncols = int(ncols)
# image = np.zeros(nrows*ncols)
# image = image.reshape((nrows,ncols))
# for game in scores_df.values:
#     image[game[0], game[1]] += 1
# row_labels = range(nrows)
# col_labels = range(ncols)
# plt.matshow(image)
# plt.xticks(range(ncols), col_labels)
# plt.yticks(range(nrows), row_labels)
# plt.show()

# Create list of missing scores
# missing_scores = []
# for i in range(0,nrows):
#     for j in range(0,ncols):
#         if image[i,j] == 0:
#             working = (i,j)
#             missing_scores.append(working)
            
# Plots scores yet to be seen
# image = np.zeros(nrows*ncols)
# image = image.reshape((nrows,ncols))
# for game in missing_scores:
#     image[game[0], game[1]] += 1
# row_labels = range(nrows)
# col_labels = range(ncols)
# plt.matshow(image)
# plt.xticks(range(ncols), col_labels)
# plt.yticks(range(nrows), row_labels)
# plt.show()

# Compare how many wins came from a home field advantage...
# Home = 0
# Away = 0
# Tie = 0
# for i in range(0,nrows):
#     for j in range(0,ncols):
#         if i > j:
#             Home += 1
#         elif i == j:
#             Tie += 1
#         else:
#             Away += 1
scores = {'Home':[],
          'Away':[],
          'Year':[],
          'ID':[]
          }
#while True:
current_year = datetime.datetime.now().year
games = api_instance.get_games(year = current_year)
for game_scores in games:
    if game_scores.id not in scores_df['ID'].values:
        if game_scores.home_points != None:
            scores['Home'].append(game_scores.home_points)
            scores['Away'].append(game_scores.away_points)
            scores['Year'].append(current_year)
            scores['ID'].append(game_scores.id)
            status_string = ("Beep Boop. I'm a bot. Final Score %s %d - %s %d." % (game_scores.home_team, game_scores.home_points, game_scores.away_team, game_scores.away_points))
            api.update_status(status_string)
                    
    #time.sleep(60*30)
    

scores = pd.DataFrame(scores)
scores_df = pd.concat([scores_df,scores], axis = 0)     
scores_df.to_csv('CFB_scores.csv',index=False)

scores_df = pd.read_csv('CFB_scores.csv')


