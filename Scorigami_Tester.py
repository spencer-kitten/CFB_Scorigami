# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 19:07:59 2021

@author: spenc
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# Import data
scores_df = pd.read_csv('CFB_scores.csv')

# Shows all time frequency of cfb scores
nrows = scores_df['Home'].max() + 1
nrows = int(nrows)
ncols = scores_df['Away'].max() + 1
ncols = int(ncols)
image = np.zeros(nrows*ncols)
image = image.reshape((nrows,ncols))

for game in scores_df.values:
    game = game.astype(int)
    image[game[0], game[1]] += 1
row_labels = range(nrows)
col_labels = range(ncols)
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
            
# Plots scores yet to be seen
image = np.zeros(nrows*ncols)
image = image.reshape((nrows,ncols))
for game in missing_scores:
    image[game[0], game[1]] += 1
# row_labels = range(nrows)
# col_labels = range(ncols)
# plt.matshow(image)
# plt.xticks(range(ncols), col_labels)
# plt.yticks(range(nrows), row_labels)
# plt.show()

image = pd.DataFrame(image)
image.to_csv('Missing_Scores.csv')