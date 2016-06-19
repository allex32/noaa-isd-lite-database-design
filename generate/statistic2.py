# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 02:26:46 2016
 
@author: Eugene
"""

import pandas as pd
import numpy as np
import pickle

df = pd.read_csv("res/isd-history.csv.txt")
df['BEGIN'] = pd.to_datetime(df['BEGIN'], format='%Y%M%d')
df['END'] = pd.to_datetime(df['END'], format='%Y%M%d')
#%%
years = [(1900,1950),(1950,2000),(2000,2016)]
for year_bound in years:
    df_current_year = df[df.apply(lambda row: year_bound[0]<= row['BEGIN'].year< year_bound[1] , axis = 1)]
    num_all = df_current_year.shape[0]
    num_null_arr = df_current_year.isnull().sum()
    p_is_null = num_null_arr/num_all #NOTE: ELEV-LAT-LON isnull only together, state date - almostly not null, USAF-WBAN almostly not_null together
    df_current_year = df_current_year.dropna(subset=['LAT','LON','ELEV(M)'])
    lat_lon_elev_mean = df_current_year[['LAT','LON','ELEV(M)']].mean()
    lat_lon_elev_var = df_current_year[['LAT','LON','ELEV(M)']].var()
    lat_lon_elev_min = df_current_year[['LAT','LON','ELEV(M)']].min()
    lat_lon_elev_max = df_current_year[['LAT','LON','ELEV(M)']].max()
    all_together = (p_is_null,lat_lon_elev_mean,lat_lon_elev_var, lat_lon_elev_min,lat_lon_elev_max)    
    #with open("res/station_statistic"+str(year_bound[0])+str(year_bound[1]),'wb') as handle:
        #pickle.dump(all_together,handle)