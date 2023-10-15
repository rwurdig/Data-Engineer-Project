from pyspark.sql import SparkSession

def write_to_hdfs(df, path, format="parquet", mode="append"):
    df.write \
        .format(format) \
        .mode(mode) \
        .save(path)

if __name__ == "__main__":
    spark = SparkSession.builder.appName("SecondLayerProcessing").getOrCreate()
    namenode = "hadoop-namenode:8020"

    # Read CSV from landing zone
    trips_df = spark.read.csv(
        f"hdfs://{namenode}/data/landing/tripdata/",
        header=True,
        inferSchema=True
    )

    # Write to bronze layer as Parquet
    bronze_path = f"hdfs://{namenode}/data/bronze/tripdata/"
    write_to_hdfs(trips_df, bronze_path)
