-- SQL Query to Fetch Distinct Regions from raw_datatrips Where Datasource is 'cheap_mobile'

-- Grouping Trips

SELECT origin_coord, destination_coord, time_of_day, COUNT(*) as num_trips
FROM datatrip
GROUP BY origin_coord, destination_coord, time_of_day;


-- Weekly Average Number of Trips

SELECT AVG(num_trips), EXTRACT(WEEK FROM created_at) as week
FROM datatrip
WHERE ST_Within(origin_coord, ST_GeomFromText('POLYGON((...))'))
GROUP BY week;
