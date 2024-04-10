import pandas as pd
from sqlalchemy import create_engine
from time import time
from datetime import datetime
import argparse

def main(params):
    user = params.user
    password = params.password
    #host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    
    # Set up connection to the Database
    engine = create_engine(f'postgresql://{user}:{password}@localhost:{port}/{db}')

    #set up an iterative dataframe to test pushing things in chunks, set to 100 for testing purposes
    df_iter = pd.read_csv('../data/illegal_dumping.csv', iterator=True, chunksize=100)

    #loop to push the data into the database
    while True:
        try:
            # starts timer for how long the loop took
            t_start = time()
            df = next(df_iter)

            # Define the date columns that need conversion
            date_columns = ['DATETIMERECEIVEDUTC', 'DATETIMECOMPLETEDUTC', 'DATETIMERECEIVED', 'DATETIMECOMPLETED', 'LASTUPDATETHIRTYDAYS', 'LASTUPDATE']

            # Convert date columns from milliseconds since Unix epoch to datetime objects
            for col in date_columns:
                df[col] = df[col].apply(lambda x: datetime.utcfromtimestamp(x / 1000) if pd.notnull(x) else pd.NaT)
            #Appends the data to the Illegal_dumping table if the table exists
            df.to_sql(name=table_name, con=engine, if_exists='append', index=False)  # Set index=False
            #stops timer for how long the loop took
            t_end = time()
            #prints how long the loop took
            print('%.3f seconds' % (t_end - t_start))
        except StopIteration:
            print("End of File")
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data in Postgres')
    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='table name where we will write results')
    #parser.add_argument('url', help='password for url to data')

    args = parser.parse_args()
    main(args)


