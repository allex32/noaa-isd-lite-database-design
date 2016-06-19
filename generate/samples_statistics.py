# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 03:01:20 2016

@author: Eugene
this file is designed to extract mean-variance-%null-min-max statistics
from the set of "samples" of noaa weather raw data
"""

import pandas as pd
import numpy as np
import pickle
import os

def lines_to_list_of_tuples(lines):
    #evil parsing byte line -> tuples 
    return [(int(line[0:4]),int(line[5:7]),int(line[8:10]),int(line[11:13]),float(line[14:19]),float(line[20:25]),float(line[26:31]),float(line[32:37]),float(line[38:43]),float(line[44:49]),float(line[50:55]),float(line[56:61])) for line in lines]
samples_dir = 'res/samples/'
os.listdir(samples_dir)
main_list = []
#%%
for file in os.listdir(samples_dir):
    with open(samples_dir+file,'rb') as f:
        lines = f.readlines()
        print(len(lines))
        main_list.extend(lines_to_list_of_tuples(lines))
df = pd.DataFrame(main_list, columns = ['year','months','day','hour','air_temp','dew_point_temp','sea_level_pressure','wind_direction','wind_speed_rate','sky_condition','liquid_precipitation_hour','liquid_precipitation_six_hours'])
df = df.replace(-9999,np.nan)
#%%
all_values = df.shape[0] #num values
null_values = df.isnull().sum()/all_values #probab for each field to be null
mean_values = df.mean() # mean values
variance_values = df.var()#variance
min_val = df.min()
max_val = df.max()
nulwith open("res/samples_stat",'wb') as f:
    pickle.dump((all_values,null_values,mean_values,variance_values,min_val,max_val),f)
    
