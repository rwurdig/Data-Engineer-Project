-- SQL Query to Fetch Distinct Regions from raw_tripsdata Where Datasource is 'cheap_mobile'
-- Using CTE for better modularity and future extensions

WITH FilteredData AS (
    -- First, filter out the data where datasource is 'cheap_mobile'
    SELECT region
    FROM raw_datatrips
    WHERE datasource = 'cheap_mobile'
),
DistinctRegions AS (
    -- Then, select distinct regions from the filtered data
    SELECT DISTINCT region
    FROM FilteredData
)
-- Final output
SELECT region
FROM DistinctRegions;
