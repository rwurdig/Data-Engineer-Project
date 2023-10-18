from pyspark.sql import SparkSession
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def write_to_postgres(df, table_name):
    df.write.format("jdbc").mode("append") \
        .option("url", f"jdbc:postgresql://jobsity-postgres:5432/jobsity") \
        .option("user", "jobsity") \
        .option("password", "jobsity") \
        .option("driver", "org.postgresql.Driver") \
        .option("dbtable", table_name) \
        .save()

def main():
    spark = SparkSession.builder.appName("PostgresIngestion").getOrCreate()

    namenode = "hadoop-namenode:8020"

    # First task
    preprocess_trips = spark.read.format("parquet").load(f"hdfs://{namenode}/data/silver/datatrip/")
    write_to_postgres(preprocess_trips, "staging_datatrip")
    logger.info("Finished first task")

    # Second task
    preprocess_avg_trips_region = spark.read.format("parquet").load(f"hdfs://{namenode}/data/silver/avg_trips_region/")
    write_to_postgres(preprocess_avg_trips_region, "avg_trips_region")
    logger.info("Finished second task")

    # Delivering raw-data
    raw_data_trip = spark.read.format("parquet").load(f"hdfs://{namenode}/data/silver/rawdatatrip/")
    write_to_postgres(raw_data_trip, "raw_datatrip")
    logger.info("Finished delivering raw data")

if __name__ == "__main__":
    main()
