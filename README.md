# Scalable Geospatial Data Pipeline with Real-Time Processing Capabilities

This robust data pipeline is engineered to streamline the processing of geospatial data with high efficiency and scalability. Utilizing a powerful technology stack that includes Apache Airflow, Apache Spark, Hadoop Distributed File System (HDFS), and PostgreSQL, the pipeline is designed to handle complex data workflows. A key feature is its integration with an Apache Airflow Directed Acyclic Graph (DAG), which automates the data processing pipeline by triggering specific tasks upon the arrival of new data files in HDFS.

# Data Flow

- Ingestion: Data is ingested into HDFS and initially processed in a landing zone.
- Optimization: Data is moved to a second layer and stored in an optimized Parquet format.
- Validation: Data validation and cleansing rules are applied.
- Staging: The cleansed data is moved to a staging table in PostgreSQL for analytical storage. Further transformations are applied, including parsing coordinate columns into PostGIS type columns.

The pipeline also includes a Flask API to expose the data stored in PostgreSQL.

# How to use
## Prerequisites

1. Make sure you have [git](https://git-scm.com/downloads) installed.
2. Make sure you have [Docker](https://docs.docker.com/engine/install/) installed.
3. Clone the project:

````
git clone https://github.com/rwurdig/Data-Engineer-Project.git
````

4. Open you terminal in linux / prompt in windows
5. Drive into the Data-Engineer-Project directory:

````
cd Data-Engineer-Project
````

6. Run the commands to start the containers (make sure you are in the same directory of docker-compose.yaml):

````
docker-compose up
````
7. In the config, airflow is running in the port 8080 with user admin and password admin.
8. Find the DAG trips-processing and click on the Play Button and after in Trigger Dag.
9. Wait for the DAG sensor starts to listen to the HDFS directory.
10. If you are using Linux, open another terminal, drive into the Data-Engineer-Project folder and run the command:
````
make add-file
````
If you are using Windows, drive into the Data-Engineer-Project and run the .bat:
````
add-file.bat
````

Or just run the commands in your terminal:
````
docker cp dataset\trips.csv hadoop-namenode:\
docker exec hadoop-namenode powershell.exe -Command "hadoop dfs -mkdir -p hdfs:///data/landing/datatrip/"
docker exec hadoop-namenode powershell.exe -Command "hadoop fs -copyFromLocal /trips.csv hdfs:///data/landing/datatrip/trips.csv"

````

11. If you want to run the spark to test something, you can do this by:
````
docker exec -it spark-master bash
````
For pyspark:
``pyspark`` For scala-spark: ``spark-shell``

12.The DAG will execute in the following sequence:
````
                  +-----------------------+
                  |                       |
                  |   landing_zone_job    |
                  |                       |
                  +-----------+-----------+
                              |
                              |
                              |
                  +-----------v-----------+
                  |                       |
                  |second_layer_processing|
                  |                       |
                  +-----------+-----------+
                              |
                              |
                              |
                  +-----------v-----------+
                  |                       |
                  | third_layer_processing|
                  |                       |
                  +-----------+-----------+
                              |
                              |
                              |
                  +-----------v-----------+
                  |                       |
                  | postgre_ingestion_job |
                  |                       |
                  +-----------+-----------+
                              |
                              |
                              |
                  +-----------v------------+
                  |                        |
                  |  _table_creation   |
                  |                        |
                  +------------+-----------+
                               |
                               |
                               |
                  +------------v-----------+
                  |                        |
                  |   _table_loading   |
                  |                        |
                  +------------------------+


````

Wait for it to finish the execution.

13.To check the Spark UI go: [http://localhost:8888](http://localhost:8888)

14.Connecting in to the PostgreSQL:

````
docker exec -it jobsity-postgres bash
psql --username=jobsity
\c jobsity
select * from staging_data limit 10;
select * from data limit 10;
select * from raw_data limit 10;
````

15.Connect to the API to get weekly avg with a bounding box.

````
wget http://localhost:50555/
````
Also, there is a table that can calculate this in the processing time
````
select * from avg_s_region;
````


## Services and ports used in the project

````
Service: api
  Exposed Port: 50555

Service: spark-master
  Exposed Port: 8888
  Internal Port: 8080
  Internal Port: 7077

Service: spark-worker
  Exposed Port: 8081
  Internal Port: 8081

Service: jobsity-postgres
  Exposed Port: 5433

Service: airflow-postgres
  Exposed Port: 5432

Service: redis
  Exposed Port: 6379

Service: webserver
  Exposed Port: 8080

Service: flower
  Exposed Port: 5555

Service: hadoop-namenode
  Exposed Port: 9870
  Exposed Port: 8020
  Exposed Port: 50070

Service: hadoop-datanode
  Internal Port: 9864
  Internal Port: 9866
  Internal Port: 9867
  Internal Port: 9868
  Internal Port: 9869
  Internal Port: 50010
  Internal Port: 50020
  Internal Port: 50075
  Internal Port: 50090

````


# To do:
````
1. Create a container with HashiCorp Vault and uses the vault to retrieve password for the server
2. Upgrade the format parquet into delta-table and use mergeSchema in the tables to update the tables
3. For simplicity, all the data is loaded at every execution, with delta-table we could upgrade to have a feature of incremental loads.
4. Implement in cloud infrastrucutre as we can see in the next section.
````

# AWS Infra

![Infrastructure on AWS](/img/aws.png)

The proposed infrastructure for the data pipeline consists of various AWS services. Airflow would be deployed on Amazon Elastic Container Service (ECS), which is a fully-managed container orchestration service that allows us to run, stop, and manage Docker containers on a cluster. Airflow can be deployed in a Docker container on ECS and managed using Amazon Elastic Kubernetes Service (EKS).

For storage, we would use Amazon Simple Storage Service (S3), which is an object storage service that offers industry-leading scalability, data availability, security, and performance. We can store the input data files on S3 and create an S3 notification event that will trigger the DAG when a new file is uploaded.

The database would be an Amazon Relational Database Service (RDS), which is a managed database service that makes it easy to set up, operate, and scale a relational database in the cloud. We can use PostgreSQL as the database for storing the processed data.

To cache and store the results of intermediate computations, we can use Amazon ElastiCache for Redis, which is an in-memory data store that provides low-latency access to frequently requested data.

For big data processing, we can use Amazon Elastic MapReduce (EMR), which is a fully-managed big data processing service that makes it easy to process large amounts of data using Spark, Hadoop, or other big data frameworks. We can create and destroy EMR clusters on the DAG to avoid having a Spark cluster always on, which can help reduce costs.

To trigger the DAG whenever a new file is uploaded to S3, we can create an S3 notification event using Amazon Simple Notification Service (SNS), which is a flexible, fully-managed pub/sub messaging and mobile notifications service for coordinating the delivery of messages to subscribing endpoints.

Overall, this infrastructure is highly scalable and flexible, making it well-suited to handle large volumes of data and accommodate future growth.


# Azure Infra

![Infrastructure on Azure](/img/Azure.png)

The proposed infrastructure on Azure would involve deploying Airflow on Azure Kubernetes Service (AKS), using Azure Blob Storage as the storage solution, and Azure Database for PostgreSQL as the database. Redis could be provisioned as a managed service, such as Azure Cache for Redis, and the Spark Cluster could be deployed on Azure HDInsight.

We could also use Azure Event Grid to trigger the DAG when a new file is uploaded to Blob Storage. This would involve creating a Blob Storage trigger that would send an event to Event Grid, which in turn could trigger the DAG.

Similar to AWS, we can also create and destroy HDInsight clusters as needed to avoid having a Spark cluster always on, and to minimize costs. This can be achieved by creating a DAG that spins up a new HDInsight cluster when needed and tears it down when it's no longer required. We can also make use of Azure Data Factory to orchestrate data movement and processing within the pipeline.

# Bonus features

• The solution is containerized

• There are two different cloud solutions

• There is a directory called SQL in the root of the project with both .sql files answering the questions:
````
From the two most commonly appearing regions, which is the latest datasource?

What regions has the "cheap_mobile" datasource appeared in?
````

# Explanation

When you run ``docker-compose up`` inside the data-engineering-challenge directory, it will start the Docker with the services and ports configured as it was shown in the previous section.

The ``localhost:8080`` is configured to the webserver of the airflow UI, where we can start the dags and check if our ingestion and processing was finished.

The ``localhost:8888`` is configured to the SparkUI, where we can see the running applications, completed applications, workers and everything related to the spark.

The ``localhost:5555`` is configured to the web interface of the Flower UI service, that is a web-based tool that provides real-time view of the tasks and workers in the celery-based distributed system.

The ``localhost:50555`` is the host port that is mapped to the container port 5000 for our API service.

When the airflow is ready to run, we should run the add-file.bat or the Makefile (depending if you are in ``windows`` or ``linux``) to copy the data inside the directory dataset to the landing zone in the HDFS.
It was designed to follow the architecture layers of a data lake, which consists in a landing zone, bronze layer, silver layer and gold layer. In this project, the landing zone inside the HDFS means that the data will be as equal as it was in the source.
The ``second_layer_processing_job`` will be responsible to get the data from the landing zone and format it into a parquet into the bronze zone and no other transformations will be made in that layer.
The ``third_layer_processing_job`` will be responsible to make the data transformations, to set up and convert the schemas and data types and save it into the silver layer of the storage.
The ``postgre_ingestion_job`` will be responsible for the last layer of our project, which instead of being a hdfs layer, we decided to use it as an analytical layer inside a postgre to have a better performance on the queries.

When you click to trig the DAG in Airflow, a sequence of ingestion and processing will start. The DAG controls that sequence of processing and one processing will only start when the previous one finishes. We configured for an auto retry once 1 minute after the failure.

While this is occurring, the API made with Flask is still running and waiting for a request. When you make the wget request as said in the previous section, it will send a rest request to the rest api and run the query inside the postgre that were configured and will retrieve the response for the question of the challenge.

Also, while everything is running, the hadoop, spark, and airflow are still running and you can use it as you want. If you need to access spark to test anything about it, you can access it by:
````
docker exec -it spark-master bash
````

Also, you can use the HDFS as a store. The ``Makefile`` and ``add-file.bat`` have examples of how to copy files to the hdfs such a csv, it is like:
````
docker cp dataset\s.csv hadoop-namenode:\
docker exec hadoop-namenode bash -c "hadoop dfs -mkdir -p hdfs:///data/landing/datatrip/"
docker exec hadoop-namenode bash -c "hadoop fs -copyFromLocal /trips.csv hdfs:///data/landing/datatrip/trips.csv"
````

You just have to pay attention in your OS, the commands can change a bit depending on the OS you are running.


Since the tools and technologies used in this project are all focused on big data and everyone has it own prove of scalability, by the usage of spark and HDFS and since it is a distributed system, the scalability of the solution is proven by itself just by the usage of every technology here.
