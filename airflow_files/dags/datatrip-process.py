# Import Required Libraries
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy import DummyOperator 
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
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
    "email_on_failure": True,  # Email notifications
    "email_on_retry": False,
    "retries": 1,
    "is_paused_upon_creation": False,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    'datatrip_ingestion',
    default_args=default_args,
    description='Automated Data Ingestion for Trip Data',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

# Python Functions
import psycopg2

def ingest_data_into_sql():
    conn = psycopg2.connect(
        host="your_host",
        database="your_database",
        user="your_username",
        password="your_password"
    )
    cursor = conn.cursor()
    
    # Your SQL INSERT logic here
    insert_query = "INSERT INTO your_table (column1, column2) VALUES (%s, %s)"
    data_to_insert = ("value1", "value2")
    
    cursor.execute(insert_query, data_to_insert)
    conn.commit()
    
    cursor.close()
    conn.close()


def validate_data():
    conn = psycopg2.connect(
        host="your_host",
        database="your_database",
        user="your_username",
        password="your_password"
    )
    cursor = conn.cursor()
    
    # Your SQL SELECT logic here to validate data
    select_query = "SELECT COUNT(*) FROM your_table WHERE some_condition"
    
    cursor.execute(select_query)
    result = cursor.fetchone()
    
    if result[0] == 0:
        raise Exception("Data validation failed: No records found based on the condition.")
    
    cursor.close()
    conn.close()

# Dummy Operators
start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)
end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

# Python Operators
ingest_operator = PythonOperator(
    task_id='Ingest_data_to_SQL',
    python_callable=ingest_data_into_sql,
    dag=dag,
)

validate_operator = PythonOperator(
    task_id='Validate_data',
    python_callable=validate_data,
    dag=dag,
)

# HDFS Sensor
landing_zone = HdfsSensor(
    task_id='landing_zone',
    filepath='/data/raw/datatrip',
    hdfs_conn_id='hdfs_default'
)

# Spark Jobs
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

# Postgres Operators
trip_table_creation = PostgresOperator(
    task_id="trip_table_creation",
    postgres_conn_id="postgres_default",
    sql="sql/datatrip_schema.sql"
)

trip_table_loading = PostgresOperator(
    task_id="trip_table_loading",
    postgres_conn_id="postgres_default",
    sql="INSERT INTO datatrip SELECT * FROM staging_tripdata;"
)

# DAG dependencies
landing_zone >> second_layer_processing_job >> third_layer_processing_job >> trip_table_creation >> trip_table_loading >> validate_operator
start_operator >> ingest_operator >> validate_operator >> end_operator
