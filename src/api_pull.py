"""
Lasted updated
2024-02-08
"""
import os
import pandas as pd
import requests
from datetime import datetime, timezone, timedelta

"""
Code was asited by chatGPT; prompt focused on converted unix time into pst. Line 13 was fixed to convert to milliseconds and 21 was generated  to convert to PST

Then I converted those lines into a function to convert columns as needed.
Since this is in San Jose I assume the timezone was in PST
"""
def convert_time(col):
    # Assuming the columns with Unix time are in milliseconds; dates make more sense with this method
    df[f'{col}'] = pd.to_datetime(df[f'{col}'] / 1000, unit='s')

    # Assuming your original time is in UTC
    utc_timezone = timezone.utc
    pst_timezone = timezone(timedelta(hours=-8))  # Pacific Standard Time (PST)

    # Convert UTC time to PST
    df[f'{col}'].dt.tz_localize(utc_timezone).dt.tz_convert(pst_timezone)
    return df
    # Now df[f'col'] contains the datetime with PST timezone
"""
This script is used to create an initial file for records on illegal dumping in the city of San Jose, California. If a file exist then it simplyy loads the CSV. The future goal is to identify how to create a filtered query to update new records. Currently I need to examine how to pull records past the newest date from whats in the datebase.


"""
file_path = '../data/illegal_dumping.csv'
if not os.path.exists(file_path):
    url = 'https://geo.sanjoseca.gov/server/rest/services/OPN/OPN_OpenDataService/MapServer/458/query?where=1%3D1&outFields=*&outSR=4326&f=json'
    req = requests.get(url)
    sj = req.json()
    result_entries = []

    for response in sj['features']:
        # Create a DataFrame with the first column and exclude the last two rows
        entry = pd.DataFrame(response).iloc[:-2, :1].transpose()

        # Append the transposed entry to the result_entries list
        result_entries.append(entry)

    # Concatenate all entries into a single DataFrame
    df = pd.concat(result_entries, ignore_index=True)

    # Reset the index of the final result_df
    df.reset_index(drop=True, inplace=True)
    #list columns of fields that should be dates
    cols = ['DATETIMERECEIVEDUTC', 'DATETIMECOMPLETEDUTC', 'DATETIMERECEIVED', 'LASTUPDATETHIRTYDAYS', 'LASTUPDATE']    
    #loop through list od columns
    for i in cols:
        #uses function to convert to time into a human readable format
        convert_time(i)
    #saves csv
    df.to_csv('../data/illegal_dumping.csv', index= False)
    #print a status code for creating a csv if it didnt exist before
    print('illegal dumping csv created')
#if the file exist then it loads it as a csv.
else:
    df= pd.read_csv('../data/illegal_dumping.csv')
    print('illegal dumping csv loaded')