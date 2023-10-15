from airflow import DAG
from airflow.operators.dummy import DummyOperator 
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator  # Updated import path
from airflow.providers.apache.hdfs.sensors.hdfs import HdfsSensor
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

# Parameters
spark_master = "spark://spark-master:7077"
spark_app_name = "Trips Process"

# DAG Definition
now = datetime.now()

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(now.year, now.month, now.day),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "is_paused_upon_creation": False,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    "trips-processing",
    default_args=default_args,
    schedule_interval=timedelta(days=1),  # Explicitly mention the unit for better readability
    catchup=False,  # Disable catchup if not needed
) as dag:

    # HDFS Sensor to monitor file arrival in HDFS
    landing_zone = HdfsSensor(
        task_id='landing_zone',
        filepath='/data/raw/datatrip',
        hdfs_conn_id='hdfs_default'
    )

    # Spark Job for data preprocessing
    second_layer_processing_job = SparkSubmitOperator(
        task_id="second_layer_processing_job",
        application="/usr/local/spark/app/second_layer_processing_job.py",
        name=spark_app_name,
        conn_id="spark_default",
        verbose=1,
        conf={"spark.master": spark_master},
        application_args=[],
        executor_memory="2G",
        executor_cores=1,
        num_executors=1
    )

    third_layer_processing_job = SparkSubmitOperator(
        task_id="third_layer_processing_job",
        application="/usr/local/spark/app/third_layer_processing_job.py",
        name=spark_app_name,
        conn_id="spark_default",
        verbose=1,
        conf={"spark.master": spark_master},
        application_args=[],
        executor_memory="2G",
        executor_cores=1,
        num_executors=1
    )

    # Spark Job for data ingestion into Postgres
    postgre_ingestion_job = SparkSubmitOperator(
        task_id="postgre_ingestion_job",
        application="/usr/local/spark/app/postgre_ingestion_job.py",
        name=spark_app_name,
        conn_id="spark_default",
        verbose=1,
        conf={"spark.master": spark_master},
        jars="/opt/postgresql-42.3.5.jar",
        application_args=[],
        executor_memory="2G",
        executor_cores=1,
        num_executors=1
    )

    # Task to create the tripdata table in Postgres
    trip_table_creation = PostgresOperator(
        task_id="trip_table_creation",
        postgres_conn_id="postgres_default",
        sql="sql/datatrip_schema.sql"
    )

    # Task to move the data from the staging_datatrip to the datatrip table
    trip_table_loading = PostgresOperator(
        task_id="trip_table_loading",
        postgres_conn_id="postgres_default",
        sql="INSERT INTO datatrip SELECT region, ST_GeomFromText(origin_coord, 4326), ST_GeomFromText(destination_coord, 4326), time_of_day, trips FROM staging_tripdata;"
    )

    # DAG dependencies
    landing_zone >> second_layer_processing_job >> third_layer_processing_job >> postgre_ingestion_job >> trip_table_creation >> trip_table_loading
