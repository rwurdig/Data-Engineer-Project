@echo off
setlocal

:: Variables
set DATASET_DIR=dataset
set CSV_FILE=trips.csv
set DOCKER_CONTAINER=hadoop-namenode
set HDFS_DIR=hdfs:///data/landing/tripdata/

:: Check if the dataset directory exists
if not exist "%DATASET_DIR%\" (
    echo Error: Dataset directory does not exist.
    exit /b 1
)

:: Check if the CSV file exists in the dataset directory
if not exist "%DATASET_DIR%\%CSV_FILE%" (
    echo Error: CSV file does not exist in the dataset directory.
    exit /b 1
)

:: Copy the CSV file to the Docker container
docker cp "%DATASET_DIR%\%CSV_FILE%" "%DOCKER_CONTAINER":\

:: Check the last command's exit code and exit if it failed
if errorlevel 1 (
    echo Error: Failed to copy the CSV file to the Docker container.
    exit /b 1
)

:: Create the HDFS directory if it doesn't exist
docker exec %DOCKER_CONTAINER% bash -c "hadoop dfs -mkdir -p %HDFS_DIR%"

:: Copy the CSV file from the Docker container to HDFS
docker exec %DOCKER_CONTAINER% bash -c "hadoop fs -copyFromLocal /%CSV_FILE% %HDFS_DIR%%CSV_FILE%"

:: Check the last command's exit code and exit if it failed
if errorlevel 1 (
    echo Error: Failed to copy the CSV file to HDFS.
    exit /b 1
)

:: Success message
echo File successfully copied to HDFS.

:: End of script
endlocal
