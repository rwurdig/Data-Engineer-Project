-- create table of the trip data
CREATE TABLE IF NOT EXISTS datatrip (
    id SERIAL PRIMARY KEY,  -- Adding a primary key for better indexing
    region VARCHAR NOT NULL,
    origin_coord GEOMETRY(Point, 4326) NOT NULL,
    destination_coord GEOMETRY(Point, 4326) NOT NULL,
    time_of_day TIME NOT NULL,
    trips BIGINT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT current_timestamp,  -- Adding a timestamp for record tracking
    INDEX idx_region (region),  -- Creating an index on 'region'
    INDEX idx_time_of_day (time_of_day),  -- Creating an index on 'time_of_day'
    SPATIAL INDEX sp_idx_origin_coord (origin_coord),  -- Creating a spatial index on 'origin_coord'
    SPATIAL INDEX sp_idx_destination_coord (destination_coord)  -- Creating a spatial index on 'destination_coord'
) PARTITION BY RANGE (created_at);  -- Partitioning the table by 'created_at' for better data management
