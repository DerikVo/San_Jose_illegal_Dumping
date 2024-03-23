import pandas as pd
from sqlalchemy import create_engine
from time import time

engine = create_engine('postgresql://postgres:admin@localhost:5432/illegal_dumping')
engine.connect()

#set up an iterative dataframe to test pushing things in chunks, set to 100 for testing purposes
df_iter = pd.read_csv('../data/illegal_dumping.csv', iterator=True, chunksize=100)

while True:
    try:
        t_start = time()
        df = next(df_iter)

        # Define the date columns that need conversion
        date_columns = ['DATETIMERECEIVEDUTC', 'DATETIMECOMPLETEDUTC', 'DATETIMERECEIVED', 'DATETIMECOMPLETED', 'LASTUPDATETHIRTYDAYS', 'LASTUPDATE']

        # Convert date columns from milliseconds since Unix epoch to datetime objects
        for col in date_columns:
            df[col] = df[col].apply(lambda x: datetime.utcfromtimestamp(x / 1000) if pd.notnull(x) else pd.NaT)

        df.to_sql(name='Illegal_Dumping', con=engine, if_exists='append', index=False)  # Set index=False

        t_end = time()

        print('%.3f seconds' % (t_end - t_start))
    except StopIteration:
        print("End of File")
        break