# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 01:54:59 2016

@author: Eugene
this file is designed to generate and insert into MS_SQL server database synthetic metadata.
generator is based on some statistics metadata coming from "samples_statistics","statistics","statistics2"
"""
#%%
import re
country_file="res/country_codes.txt"
country_codes = open(country_file,"r")
country_lines = country_codes.readlines()[2:]
country_codes_list = [re.sub('[\s+]', ' ', line).rstrip()[:2] for line in country_lines]
country_codes.close()
from random import shuffle
shuffle(country_codes_list)
#%%
from datetime import timedelta, date

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
#%%
import numpy as np
import pickle 
import datetime

import pyodbc
cnxn = pyodbc.connect(r'Driver={SQL Server};Server=localhost\SQLEXPRESS;Database=NOAA;Trusted_Connection=yes;')
cursor = cnxn.cursor()
#%%
raw_weather_id = 0
weather_station_id = 0
num_countries = 150
year_bounds = [(2000,2016)] #generate only for 2000-2016
counter_for_name=0
counter_for_call_sign = 0
USAF = 0
WBAN = 0
hours_ranges=[1,3,6]
time1 = datetime.datetime.now()
#%%
for year_bound in year_bounds:
    num_stations = []    
    with open("res/num_stations_list",'rb') as f:
        num_stations = pickle.load(f)[2] #hardcode because i can =) 
    p_is_null_country = 0
    cumsum=[]
    bins=[]
    with open("res/country_num_statuions"+str(year_bound[0])+str(year_bound[1]),'rb') as f:
        (p_is_null_country, cumsum, bins) = pickle.load(f)

    cumsum = np.insert(cumsum,0.0,0)
    cumsum_temp=[]
    for i in range(0,len(cumsum)-1):
        cumsum_temp.append((cumsum[i],cumsum[i+1]))#python interprets range only for iterating, kek, no float-range for 0.1 in range(0.0,0.1)
    cumsum=list(enumerate(cumsum_temp)) # index - "range" for cumsum
  
    bins_temp = []
    for i in range(0,len(bins)-1):
        bins_temp.append((bins[i],bins[i+1]))
    bins=bins_temp
    
    num_all_values=0.0
    null_values={}
    mean_values={}
    variance_values={}
    country_num_stations_min = {}
    country_num_stations_max = {}
    with open("res/samples_stat",'rb') as f:
        (num_all_values,null_values,mean_values,variance_values,country_num_stations_min,country_num_stations_max) = pickle.load(f)
    
    p_is_null = 0.0
    lat_lon_elev_mean={}
    lat_lon_elev_var={}
    lat_lon_elev_min={}
    lat_lon_elev_max={}
    with open("res/station_statistic"+str(year_bound[0])+str(year_bound[1]),'rb') as f:
        (p_is_null,lat_lon_elev_mean,lat_lon_elev_var,lat_lon_elev_min,lat_lon_elev_max) = pickle.load(f)
    for country_number in range(0,num_countries+1):
        first_rand = np.random.uniform()
        bounds_num_stations_index = next(x for x in cumsum if x[1][0]<=0.5<x[1][1])[0]
        bounds_num_stations = bins[bounds_num_stations_index]
        num_stations = np.random.uniform(bounds_num_stations[0],bounds_num_stations[1])
        if(country_number==num_countries):
            num_stations = 3500
        for station_number in range(int(num_stations)):
            name = ""
            if (np.random.uniform()<p_is_null['STATION NAME']):
                name = None
            else:
                name = "station_name_"+str(counter_for_name)
                counter_for_name = counter_for_name + 1
            
            usaf_wban = ""
            if (np.random.uniform()>0.5):
                usaf_wban = str(USAF).zfill(6)+"-99999"
                USAF = USAF +1
            else:
                usaf_wban = "999999-"+str(WBAN).zfill(5)
                WBAN = WBAN+1
            
            lat = 0.0
            lon = 0.0
            elev = 0.0
            if (np.random.uniform()<p_is_null['LAT']):
                lat = None
                lon = None
                elev = None
            else:
                lat = np.random.uniform(lat_lon_elev_min['LAT'],lat_lon_elev_max['LAT'])
                lon = np.random.uniform(lat_lon_elev_min['LON'],lat_lon_elev_max['LON'])
                elev = np.random.uniform(lat_lon_elev_min['ELEV(M)'],lat_lon_elev_max['ELEV(M)'])
            
            call_sign = ""        
            if (np.random.uniform()<p_is_null['ICAO']):
                call_sign = None
            else:
                call_sign = str("cs")+str(counter_for_call_sign)
                counter_for_call_sign = counter_for_call_sign +1
            state = ""
            
            zero_date = datetime.datetime.strptime('2000', '%Y')
            days_from_zero = int(np.random.uniform(0,365*16))
            last_days = int(np.random.uniform(0,365*16+300 - days_from_zero)) # a bit of dirty magic =)
            
            begin_date = zero_date+ datetime.timedelta(days = days_from_zero)
            end_date = begin_date+datetime.timedelta(days = last_days)   
            
            ctry = country_codes_list[0]
            cursor.execute("SET IDENTITY_INSERT Weather_station ON;")
            cursor.commit()
            cursor.execute("INSERT INTO Weather_station( id_weather_station,name, country_code, state_code, call_sign, lat, long, elevation, usaf_wban)VALUES(?,?,?,?,?,?,?,?,?)",
                           weather_station_id,                            
                           name,
                           ctry,
                           state,
                           call_sign,
                           lat,
                           lon,
                           elev,
                           usaf_wban)
            cursor.execute("SET IDENTITY_INSERT Weather_station OFF;")
            cursor.commit()
            delta_hours = int((end_date-begin_date).total_seconds()/(60*60))
            hours_range = hours_ranges[int(np.random.uniform(0,3))]
            
            temp_mean = np.random.uniform(country_num_stations_min['air_temp'],country_num_stations_max['air_temp'])
            temp_variance = np.random.uniform(0,1.5*variance_values['air_temp'])
            
            pressure_mean = np.random.uniform(country_num_stations_min['sea_level_pressure'],country_num_stations_max['sea_level_pressure'])
            pressure_variance = np.random.uniform(0,1.5*variance_values['sea_level_pressure'])                
                 
            dewpoint_mean = np.random.uniform(country_num_stations_min['dew_point_temp'],country_num_stations_max['dew_point_temp'])
            dewpoint_variance = np.random.uniform(0,1.5*variance_values['dew_point_temp'])                

            wind_direction_mean = np.random.uniform(country_num_stations_min['wind_direction'],country_num_stations_max['wind_direction'])
            wind_direction_variance = np.random.uniform(0,1.5*variance_values['wind_direction'])                

            wind_speed_rate_mean = np.random.uniform(country_num_stations_min['wind_speed_rate'],country_num_stations_max['wind_speed_rate'])
            wind_speed_rate_variance = np.random.uniform(0,1.5*variance_values['wind_speed_rate'])                

            sky_condition_mean = np.random.uniform(country_num_stations_min['sky_condition'],country_num_stations_max['sky_condition'])
            sky_condition_variance = np.random.uniform(0,1.5*variance_values['sky_condition'])                
       
            liquid_precipitation_hour_mean = np.random.uniform(country_num_stations_min['liquid_precipitation_hour'],country_num_stations_max['liquid_precipitation_hour'])
            liquid_precipitation_hour_variance = np.random.uniform(0,1.5*variance_values['liquid_precipitation_hour'])                
            
            liquid_precipitation_six_hours_mean = np.random.uniform(country_num_stations_min['liquid_precipitation_six_hours'],country_num_stations_max['liquid_precipitation_six_hours'])
            liquid_precipitation_six_hours_variance = np.random.uniform(0,1.5*variance_values['liquid_precipitation_six_hours'])                
                  
            cursor.commit()
            cursor.execute("SET IDENTITY_INSERT [dbo].[Raw_weather_data] ON;")
            cursor.commit()
            for hour in range(0,delta_hours,hours_range): #generating raw data
                time = begin_date + timedelta(hours = hour)
                
                                
                temperature = None
                if(null_values['air_temp']<=np.random.uniform()):
                    temperature = np.random.normal(loc = temp_mean, scale = np.sqrt(temp_variance))
                
                dewpoint = None
                if(null_values['dew_point_temp']<=np.random.uniform()):
                    dewpoint = np.random.normal(loc = dewpoint_mean, scale = np.sqrt(dewpoint_variance))
                
                pressure = None
                if(null_values['dew_point_temp']<=np.random.uniform()):
                    pressure = np.random.normal(loc = pressure_mean, scale = np.sqrt(pressure_variance))
                
                wind_direction = None
                if(null_values['wind_direction']<=np.random.uniform()):
                    wind_direction = int(np.random.normal(loc = wind_direction_mean, scale = np.sqrt(wind_direction_variance)))
                
                sky_condition = None
                if(null_values['sky_condition']<=np.random.uniform()):
                    sky_condition = int(np.random.normal(loc = sky_condition_mean, scale = np.sqrt(sky_condition_variance)))
                
                
                wind_speed_rate = None
                if(null_values['wind_direction']<=np.random.uniform()):
                    wind_speed_rate = np.random.normal(loc = wind_speed_rate_mean, scale = np.sqrt(wind_speed_rate_variance))
                
                liquid_precipitation_hour = None
                if(null_values['liquid_precipitation_hour']<=np.random.uniform()):
                    liquid_precipitation_hour = int(np.random.normal(loc = liquid_precipitation_hour_mean, scale = np.sqrt(liquid_precipitation_hour_variance)))
                
                liquid_precipitation_six_hours = None
                if(null_values['liquid_precipitation_six_hours']<=np.random.uniform()):
                    liquid_precipitation_six_hours = int(np.random.normal(loc = liquid_precipitation_six_hours_mean, scale = np.sqrt(liquid_precipitation_six_hours_variance)))
                     
                
                cursor.execute("INSERT INTO Raw_weather_data(id_station,time,temperature,dewpoint,pressure,wind_direction,wind_speed, sky_condition,one_hour_precip,six_hour_precip) VALUES (?,?,?,?,?,?,?,?,?,?)",
                               weather_station_id,
                               time,
                               temperature,
                               dewpoint,
                               pressure,
                               wind_direction,
                               sky_condition,
                               wind_speed_rate,
                               liquid_precipitation_hour,
                               liquid_precipitation_six_hours)
            weather_station_id = weather_station_id + 1
            cursor.execute("SET IDENTITY_INSERT [dbo].[Raw_weather_data] OFF;")
            cursor.commit()
            print(ctry +" done")
        country_codes_list = country_codes_list[1:]
cnxn.close()
time_all = datetime.datetime.now() - time1