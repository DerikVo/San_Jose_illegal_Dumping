/*
20240213

This query is designed to generate the illegaldumping table and populate the data via a CSV
However I getting:
	
	ERROR:  date/time field value out of range: "1590721500"
	HINT:  Perhaps you need a different "datestyle" setting.
	CONTEXT:  COPY illegal_dumping_temp, line 2, column datetimereceivedutc: "1590721500" 

	SQL state: 22008
	
So I will need to explore the issue im having. using a to_timestamp on the value generates a date,
and I have a python script that populates the database with insert statements that works. However,
I want to automate things as much as possible so if I can get this working this would be more efficient.
*/
-- Create the temporary or test table with UnixTime columns as TIMESTAMP WITH TIME ZONE
CREATE TABLE illegal_dumping_temp (
    datetimereceivedutc timestamptz,
    datetimecompletedutc timestamptz,
    workorderrefno varchar,
    objectid bigint,
    facilityid bigint,
    intid bigint,
    councildistrict int CHECK (councildistrict >= 0 AND councildistrict <= 10),
    servicerecordid bigint,
    servicecategory varchar,
    datetimereceived timestamptz,
    status varchar(10) CHECK (status IN ('Closed', 'Assigned', 'Open')),
    datetimecompleted timestamptz,
    detailsummary varchar,
    latitude numeric,
    longitude numeric,
    imagename varchar,
    hyperlink varchar,
    mysanjoserefno varchar,
    lastupdatethirtydays timestamptz,
    lastupdate timestamptz,  
    notes varchar,
    enterpriseid varchar,
    globalid varchar
);

-- Load data from CSV using Unix time into the temp table
COPY illegal_dumping_temp (
    datetimereceivedutc,
    datetimecompletedutc,
    workorderrefno,
    objectid,
    facilityid,
    intid,
    councildistrict,
    servicerecordid,
    servicecategory,
    datetimereceived,
    status,
    datetimecompleted,
    detailsummary,
    latitude,
    longitude,
    imagename,
    hyperlink,
    mysanjoserefno,
    lastupdatethirtydays,
    lastupdate,
    notes,
    enterpriseid,
    globalid
) 
FROM '..\San_Jose_illegal_Dumping\data\illegal_dumping.csv' DELIMITER ',' CSV HEADER;

-- Update the existing timestamptz columns using Unix time
UPDATE 
	illegal_dumping_temp 
SET 
	datetimereceivedutc = to_timestamp(datetimereceivedutc),
    datetimecompletedutc = to_timestamp(datetimecompletedutc),
    lastupdatethirtydays = to_timestamp(lastupdatethirtydays),
    lastupdate = to_timestamp(lastupdate);
