/*
This table is used to store data from the San Jose illegal dumping API

The api pull does light cleaning such as coverting data from unix to utc pst date time format

*/

CREATE TABLE illegal_dumping (
    datetimereceivedutc timestamptz
    ,datetimecompletedutc timestamptz
    ,workorderrefno varchar
    ,objectid bigint
    ,facilityid bigint
    ,intid bigint
    ,councildistrict int CHECK (councildistrict >= 0 AND councildistrict <= 10)
    ,servicerecordid bigint
    ,servicecategory varchar
    ,datetimereceived timestamptz
    ,status varchar(10) CHECK (status IN ('Closed', 'Assigned', 'Open'))
    ,datetimecompleted timestamptz
    ,detailsummary varchar
    ,latitude numeric
    ,longitude numeric
    ,imagename varchar
    ,hyperlink varchar
    ,mysanjoserefno varchar
    ,lastupdatethirtydays timestamptz
    ,lastupdate timestamptz
    ,notes varchar
    ,enterpriseid varchar
    ,globalid varchar
);