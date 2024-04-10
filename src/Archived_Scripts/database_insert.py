"""
Last updated: 20240219

This script is a work around for inserting data into the database with individual insert statements. Currently have isues with using the import function and date's being out of range. Even when converting them to seconds or using date strings via api protocol. 

"""
import pandas as pd
import numpy as np

def generate_insert_sql(df, table_name, output_file):
    df.replace(np.nan, 0, inplace=True) #temporary fix to get pipeline to work; will need to fix later
    # Open the SQL file we will use to populate the datebase
    with open(output_file, 'w') as sql_file:
        # Iterate through the DataFrame rows
        for index, row in df.iterrows():
            #get rid of quotes so the program doesnt break
            row = row.apply(lambda x: str(x).replace("'", "''").replace('"', '""'))
            #drops nan strings

            # Construct the SQL insert statement for each row
            sql = f"INSERT INTO {table_name} (DATETIMERECEIVEDUTC, DATETIMECOMPLETEDUTC, WORKORDERREFNO, OBJECTID, FACILITYID, INTID, COUNCILDISTRICT, SERVICERECORDID, SERVICECATEGORY, DATETIMERECEIVED, STATUS, DATETIMECOMPLETED, DETAILSUMMARY, LATITUDE, LONGITUDE, IMAGENAME, HYPERLINK, MYSANJOSEREFNO, LASTUPDATETHIRTYDAYS, LASTUPDATE, NOTES, ENTERPRISEID, GlobalID) VALUES "
            sql += f"(to_timestamp('{row['DATETIMERECEIVEDUTC']}'), to_timestamp('{row['DATETIMECOMPLETEDUTC']}'), '{row['WORKORDERREFNO']}', '{row['OBJECTID']}', '{row['FACILITYID']}', '{row['INTID']}', '{row['COUNCILDISTRICT']}', {row['SERVICERECORDID']}, '{row['SERVICECATEGORY']}', to_timestamp('{row['DATETIMERECEIVED']}'), '{row['STATUS']}', to_timestamp('{row['DATETIMECOMPLETED']}'), '{row['DETAILSUMMARY']}', '{row['LATITUDE']}', '{row['LONGITUDE']}', '{row['IMAGENAME']}', '{row['HYPERLINK']}', '{row['MYSANJOSEREFNO']}', to_timestamp('{row['LASTUPDATETHIRTYDAYS']}'), to_timestamp('{row['LASTUPDATE']}'), '{row['NOTES']}', '{row['ENTERPRISEID']}', '{row['GlobalID']}');\n"
            
            # Write the SQL statement to the file
            sql_file.write(sql)

    print(f"SQL statements have been written to {output_file}")

# specifiy the file we will be using
df = pd.read_csv('../data/illegal_dumping.csv')

# Specify the table name were inserting into
table_name = 'illegal_dumping'

# Specify the output SQL file name
output_sql_file = '../src/illegal_dumping_data.sql'

# Call the function
generate_insert_sql(df, table_name, output_sql_file)