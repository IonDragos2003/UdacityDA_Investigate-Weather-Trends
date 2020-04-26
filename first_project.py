''' Importing the packages needed for the analysis '''

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Importing the London temperatures
city_temp = pd.read_csv('london.csv')
# Importing the Global temperatures
global_temp = pd.read_csv('global_temp.csv')


''' Renaming the avg_temp columns so I won't have issues when merging them'''

city_temp.rename(columns={'avg_temp': 'avg_temp_local'}, inplace=True)
global_temp.rename(columns={'avg_temp': 'avg_temp_global'}, inplace=True)

# Seeing how many null values I have for the avg_temp for both data sets
print (city_temp['avg_temp_local'].isna().sum())
print (global_temp['avg_temp_global'].isna().sum())

# Filling the missing values in the London dataset with the previous values
city_temp['avg_temp_local'].fillna(method='ffill', inplace=True)
# Checking for expected output (0)
print (city_temp['avg_temp_local'].isna().sum())


''' Creating the 7 day moving average temperatures for local and global datasets'''

city_temp['7_day_MA_local'] = city_temp['avg_temp_local'].rolling(window=7).mean()
global_temp['7_day_MA_global'] = global_temp['avg_temp_global'].rolling(window=7).mean()

''' Creating the 14 day moving average temperatures for local and global datasets'''

city_temp['14_day_MA_local'] = city_temp['avg_temp_local'].rolling(window=14).mean()
global_temp['14_day_MA_global'] = global_temp['avg_temp_global'].rolling(window=14).mean()

# Merging the dataframes into one
final_df = pd.merge(city_temp, global_temp, on = 'year')

# Given that the London dataset is starting from 1743 and the Global dataset is starting from 1750, while calculating moving averages
# there will be empty values which will result in a spike when plotted.
# As of this, I am subsetting the final dataframe into 2 separate dataframes where we start from a year where both datasets have data
final_df_7_day = final_df.iloc[6:]
final_df_14_day = final_df.iloc[13:]

# Checking for expected output
print (final_df.head(20))

# Calculating the 7 day and 14 day correlation between local and global temps
corr_7_day = final_df_7_day['7_day_MA_local'].corr(final_df_7_day['7_day_MA_global'])
corr_14_day = final_df_14_day['14_day_MA_local'].corr(final_df_14_day['14_day_MA_global'])

print (corr_7_day)
print (corr_14_day)

# Printing the two plots where we have 7 day MA for London vs 7 day MA for Global and same for 14 day. 
final_df_7_day.plot(x='year',y=['7_day_MA_local','7_day_MA_global'])
plt.ylabel ('Average temperature in ºC')
plt.title ('Avg temp in ºC as a 7-day MA for London vs Global over the years')
final_df_14_day.plot(x='year',y=['14_day_MA_local','14_day_MA_global'])
plt.ylabel ('Average temperature in ºC')
plt.title ('Avg temp in ºC as a 14-day MA for London vs Global over the years')
plt.show()