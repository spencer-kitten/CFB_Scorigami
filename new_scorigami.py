#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 14:14:41 2021

@author: spencerkitten
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import colors
import datetime as datetime
from Twitter_Access import *
import tweepy
import os

def new_scorigami(weekly_scorigami):
    # Twitter API
    auth = tweepy.OAuthHandler(API, API_S)
    auth.set_access_token(Access, Access_S)
    api = tweepy.API(auth)
    
    # Read in all scores
    winner_df = pd.read_csv('Missing_Scores2.csv')
    
    # Create array of scores
    # Each cell value storing an integer relating to freq of occurance
    nrows = winner_df['MAX'].max() + 1
    ncols = winner_df['MAX'].max() + 1
    image = np.zeros(nrows*ncols)
    image = image.reshape((nrows,ncols))
    
    for game in winner_df.values:
        image[game[2], game[1]] += 1
    
    # Create list of missing scores
    missing_scores = []
    for i in range(0,nrows):
        for j in range(0,ncols):
            if image[i,j] == 0:
                working = (i,j)
                missing_scores.append(working)
    
    # # Plots scores yet to be seen with missing values as '1'
    image2 = np.zeros(nrows*ncols)
    image2 = image2.reshape((nrows,ncols))
    for game2 in missing_scores:
        image2[game2[0], game2[1]] += 1
    
    # Missing scores are now '0' and scores that have happened are '1'
    image3 = 1-image2
    image3
    
    # Unpack dict into list of tuples
    for i in range(0,len(weekly_scorigami['ID'])):
        maxi = (weekly_scorigami['MAX'][i])
        mini = (weekly_scorigami['MIN'][i])
        working = (maxi,mini)
        weekly_list.append(working)
    
    # Add in new scorigamis 
    for game3 in weekly_scorigami:
        image3[game3[0],game3[1]] += 1
        
    row_labels = range(81)
    col_labels = range(81)
    cmap = colors.ListedColormap(['white', 'blue', 'red'])
    bounds=[0,1,2,3]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    plt.matshow(image3[0:81,0:81],cmap=cmap,norm = norm)
    plt.xticks(range(81), col_labels)
    plt.yticks(range(81), row_labels)
    #plt.show()
    #plt.savefig('test.pdf', bbox_inches='tight')
    fig1 = plt.gcf()
    fig1.set_size_inches(100, 100)
    #plt.show()
    #plt.draw()
    
    # Time Data
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    year = datetime.datetime.now().year
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    second = datetime.datetime.now().second

    # Create filename, message, savefigure, and update
    filename = ('%d%d%d%d%d%d.png' % (month,day,year,hour,minute,second))
    message = ('There is/are %d new Scorigami(s) this week, plotted in red.' % (len(weekly_scorigami_list)))
    os.chdir('PNG')
    fig1.savefig(filename, dpi=70)
    api.update_with_media(filename, status=message)
    os.chdir('..')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    