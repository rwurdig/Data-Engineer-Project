
-- SQL obtain the weekly average number of trips for an area, defined by a bounding box (given by coordinates) or by a region.

SELECT AVG(num_trips), EXTRACT(WEEK FROM created_at) as week
FROM datatrip
WHERE ST_Within(origin_coord, ST_GeomFromText('POLYGON((...))'))
GROUP BY week;
