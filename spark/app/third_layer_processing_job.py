from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def write_to_hdfs(df, path):
    df.write.format("parquet").mode("append").save(path)
    logger.info(f"Data written to {path}")

def main():
    spark = SparkSession.builder.appName("ThirdLayerProcessing").getOrCreate()
    namenode = "hadoop-namenode:8020"

    # Main table without transformation
    trips_df = spark.read.format("parquet").load(f"hdfs://{namenode}/data/bronze/tripdata/")

    # First transformation of the date
    preprocess_data = trips_df.withColumn("datetime", date_format("datetime", "yyyy-MM-dd HH:mm"))

    # First task: Grouping trips with similar origin, destination, and time of day
    preprocess_data_time_of_day = preprocess_data.withColumn("time_of_day", date_format("datetime", "HH:mm"))
    grouped_df = preprocess_data_time_of_day.groupBy("region", "origin_coord", "destination_coord", "time_of_day").agg(count("datasource").alias("trips"))
    write_to_hdfs(grouped_df, f"hdfs://{namenode}/data/silver/tripdata/")

    # Second task: Weekly average number of trips for a region
    grouped_df_avg_weeks = preprocess_data.groupBy("region", year("datetime").alias("year"), weekofyear("datetime").alias("week")).agg(count("datasource").alias("trips"))
    num_weeks = grouped_df_avg_weeks.select("year", "week").distinct().count()
    avg_trips = grouped_df.groupBy("region").agg(sum("trips").alias("total_trips")).withColumn("avg_trips", col("total_trips") / num_weeks)
    write_to_hdfs(avg_trips, f"hdfs://{namenode}/data/silver/avg_trips_region/")

    # Delivering the raw-data
    write_to_hdfs(preprocess_data, f"hdfs://{namenode}/data/silver/rawtripdata/")

if __name__ == "__main__":
    main()
