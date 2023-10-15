# Variables
NAMENODE_CONTAINER = hadoop-namenode
DATASET_DIR = dataset
CSV_FILE = trips.csv
HDFS_DIR = hdfs:///data/landing/datatrip

# Add file to HDFS
add-file: create-hdfs-dir copy-file-to-container copy-file-to-hdfs

# Create HDFS directory
create-hdfs-dir:
	@echo "Creating HDFS directory..."
	@docker exec $(NAMENODE_CONTAINER) bash -c "hadoop dfs -mkdir -p $(HDFS_DIR)"

# Copy file to Hadoop container
copy-file-to-container:
	@echo "Copying file to Hadoop container..."
	@docker cp $(DATASET_DIR)/$(CSV_FILE) $(NAMENODE_CONTAINER):/

# Copy file from container to HDFS
copy-file-to-hdfs:
	@echo "Copying file from container to HDFS..."
	@docker exec $(NAMENODE_CONTAINER) bash -c "hadoop fs -copyFromLocal /$(CSV_FILE) $(HDFS_DIR)/$(CSV_FILE)"

.PHONY: add-file create-hdfs-dir copy-file-to-container copy-file-to-hdfs
