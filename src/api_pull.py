import os
import pandas as pd
import requests

"""
20240219
Code was asited by chatGPT; prompt focused on converted unix time into pst. Line 13 was fixed to convert to milliseconds and 21 was generated  to convert to PST

Then I converted those lines into a function to convert columns as needed.
Since this is in San Jose I assume the timezone was in PST

This has gone through serval interations due to issues with importing data into postgresql


Code was later updated to have a seperate script for pulling the data an cleaning the data
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
    #saves csv
    if not os.path.exists('../data'):
        os.makedirs('../data')
    df.to_csv('../data/illegal_dumping.csv', index= False)
    #print a status code for creating a csv if it didnt exist before
    print('illegal dumping csv created')
#if the file exist then it loads it as a csv.
else:
    df= pd.read_csv('../data/illegal_dumping.csv')
    # Need to learn how to use the params with this datebase; using time and the column name is not working
    # url = 'https://geo.sanjoseca.gov/server/rest/services/OPN/OPN_OpenDataService/MapServer/458/query?where=1%3D1&outFields=*&outSR=4326&f=json'
    # newest_date = df['DATETIMERECEIVEDUTC'].max()
    # params = {'time' : newest_date+1}
    # req = requests.get(url, params=params)
    # sj = req.json()
    # result_entries = []
    # for response in sj['features']:
    #     # Create a DataFrame with the first column and exclude the last two rows
    #     entry = pd.DataFrame(response).iloc[:-2, :1].transpose()
    #     result_entries.append(entry)
    # df = pd.concat([df]+result_entries, ignore_index=True)
    print('illegal dumping csv loaded and updated')