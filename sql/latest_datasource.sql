-- SQL Query to Fetch the Latest Datasource from the Two Most Commonly Appearing Regions

WITH TopRegions AS (
    -- Identify the two most commonly appearing regions
    SELECT region
    FROM raw_datatrips
    GROUP BY region
    ORDER BY COUNT(*) DESC
    LIMIT 2
),
LatestData AS (
    -- Find the latest datetime for each datasource in the top regions
    SELECT 
        region,
        datasource,
        MAX(datetime) OVER (PARTITION BY region, datasource) AS latest_datetime
    FROM raw_datatrips
    WHERE region IN (SELECT region FROM TopRegions)
),
RankedData AS (
    -- Rank the data based on the count and latest datetime
    SELECT *,
           RANK() OVER (ORDER BY COUNT(*) DESC, latest_datetime DESC) AS rank
    FROM LatestData
    GROUP BY region, datasource, latest_datetime
)
-- Select the top-ranked record
SELECT region, datasource, latest_datetime
FROM RankedData
WHERE rank = 1;
