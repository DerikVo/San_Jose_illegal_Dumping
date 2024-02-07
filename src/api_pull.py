import pandas as pd
import requests


url = 'https://geo.sanjoseca.gov/server/rest/services/OPN/OPN_OpenDataService/MapServer/458/query?where=1%3D1&outFields=*&outSR=4326&f=json'

req = requests.get(url)

req.status_code

result_entries = []

for response in req.json()['features']:
    # Create a DataFrame with the first column and exclude the last two rows
    entry = pd.DataFrame(response).iloc[:-2, :1].transpose()
    
    # Append the transposed entry to the result_entries list
    result_entries.append(entry)

# Concatenate all entries into a single DataFrame
df = pd.concat(result_entries, ignore_index=True)

# Reset the index of the final result_df
df.reset_index(drop=True, inplace=True)

df.to_csv('../data/illegal_dumping.csv')
