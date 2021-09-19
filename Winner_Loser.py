# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 00:52:44 2021

@author: spenc
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def missing_data_builder():
    # Import data
    # scores_df = pd.read_csv('CFB_scores.csv')
    # scores_df.drop(['Home_Team'],axis=1,inplace=True)
    # scores_df.drop(['Away_Team'],axis=1,inplace=True)
    
    # winner_df = {'ID':[],
    #               'MAX':[],
    #               'MIN':[]
    #               }
    # for game in scores_df.index:
    #     maximum = max(scores_df.iloc[game]['Home'],scores_df.iloc[game]['Away'])
    #     minimum = min(scores_df.iloc[game]['Home'],scores_df.iloc[game]['Away']) 
    #     winner_df['ID'].append(scores_df.iloc[game]['ID'])
    #     winner_df['MAX'].append(maximum)
    #     winner_df['MIN'].append(minimum)
        
    # winner_df = pd.DataFrame(winner_df)
    # winner_df.to_csv('Missing_Scores2.csv')
    winner_df = pd.read_csv('Missing_Scores2.csv')
    
    nrows = int(winner_df['MAX'].max()) + 1
    ncols = int(winner_df['MAX'].max()) + 1
    image = np.zeros(nrows*ncols)
    image = image.reshape((nrows,ncols))
    
    for game in winner_df.values:
        image[game[2], game[1]] += 1
    # row_labels = range(nrows)
    # col_labels = range(ncols)
    # plt.matshow(image)
    # plt.xticks(range(ncols), col_labels)
    # plt.yticks(range(nrows), row_labels)
    # plt.show()
    
    
    # Find missing scores
    # Create list of missing scores
    missing_scores = []
    for i in range(0,nrows):
        for j in range(0,ncols):
            if image[i,j] == 0:
                working = (i,j)
                missing_scores.append(working)
                
    # # Plots scores yet to be seen
    image2 = np.zeros(nrows*ncols)
    image2 = image2.reshape((nrows,ncols))
    for game2 in missing_scores:
        image2[game2[0], game2[1]] += 1
    # row_labels = range(nrows)
    # col_labels = range(ncols)
    # plt.matshow(image2)
    # plt.xticks(range(ncols), col_labels)
    # plt.yticks(range(nrows), row_labels)
    # plt.show()
    
    image2 = pd.DataFrame(image2)
    #image.to_csv('Missing_Scores2.csv')
    
    return image2