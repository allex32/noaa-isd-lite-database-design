# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 19:58:04 2016

@author: Eugene
this file is designed to extract and save country-num_stations data from noaa isd-history.csv file and plot hist
"""

import numpy as np
from matplotlib import pyplot as plt

    
    plt.show()
def plot_hist(hist,bins, title):
    width = [(bins[i+1]-bins[i]) for i in range(0,len(bins)-1)]

    center = [(bins[i+1]-bins[i]) for i in range(0,len(bins)-1)]
    fig = plt.figure(figsize=(8, 6), dpi=80)  
    (fig, ax) = plt.subplots()
    
    ax.bar(center, hist, align='center', width=width)
    ax.set_xticks([0]+bins)
    ax.set_yticks(np.arange(0,101,10))

    ax.get_xaxis().get_major_formatter().labelOnlyBase = False

    plt.title(title)
    plt.show()

#%%

import re
country_file="res/country_codes.txt"
country_codes = open(country_file,"r")
country_lines = country_codes.readlines()[2:]
country_codes_list = [re.sub('[\s+]', ' ', line).rstrip()[:2] for line in country_lines]
country_codes.close()
#%%
import pandas as pd
isd_history = pd.read_csv('res/isd-history.csv.txt')
isd_history['BEGIN'] = pd.to_datetime(isd_history['BEGIN'], format='%Y%M%d')
isd_history['END'] = pd.to_datetime(isd_history['END'], format='%Y%M%d')
#%%
isd_meaningfull = isd_history[['STATION NAME','CTRY','BEGIN','END']]
import pickle 
from datetime import datetime
years = [(1900,1950),(1950,2000),(2000,2016)]
num_stations_in_bounds =[]

bins = [0,1,10,30,50]+list(range(100,1001,100))#bins are selected "by-an-eye"
for year_bounds in years:
    isd_current_year = isd_meaningfull[isd_meaningfull.apply(lambda row: year_bounds[0]<=row['END'].year<year_bounds[1] , axis = 1)]
    num_all = isd_current_year.shape[0]
    num_stations_in_bounds.append(num_all)    
    num_null = isd_current_year.isnull().sum()['CTRY']
    isd_current_year = isd_current_year[isd_current_year['CTRY'].notnull()]# drops null ctry        
    num_notnull = isd_current_year.shape[0]
    print(isd_current_year.shape)
    isd_grouped = isd_current_year[['CTRY','STATION NAME']].groupby(['CTRY']).agg(['count'])
        
    listVal = list(zip(isd_grouped.index.values,isd_grouped.values))
    listVal = [(l[0],l[1][0]) for l in listVal]
    
    list_non_missed = list(isd_grouped.index.values) #replaceing missed values by 0
    missedZeroes = [(code,0) for code in country_codes_list if code not in list_non_missed] 
    
    final = listVal + missedZeroes
    hist, bins = np.histogram([el[1] for el in final], bins = bins)
    cumsum = np.cumsum(hist)/len(country_codes_list)
    p_is_null = num_null/num_all
    all_together = (p_is_null, cumsum, bins)
    with open('res/country_num_statuions'+str(year_bounds[0])+str(year_bounds[1]),'wb') as handle:
        pickle.dump(all_together,handle)
    #plot_hist(hist,bins, str(year_bounds))
        
    print(listVal[0])
with open('res/num_stations_list','wb') as handle:
    pickle.dump(num_stations_in_bounds,handle)