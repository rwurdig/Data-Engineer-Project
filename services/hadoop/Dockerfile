# Use a base image with OpenJDK and a minimal OS
FROM openjdk:8-slim

# Set environment variables for Hadoop
ENV HADOOP_VERSION=3.2.1 \
    HADOOP_HOME=/usr/local/hadoop \
    HADOOP_OPTS="-Djava.library.path=/usr/local/hadoop/lib/native" \
    HADOOP_USER_NAME=hdfs \
    HDFS_NS=hdfs://hdfs

# Update and install necessary packages
RUN apt-get update && \
    apt-get install -y wget netcat-openbsd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Download and install Hadoop
RUN wget -q https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz && \
    tar -xzf hadoop-${HADOOP_VERSION}.tar.gz -C /usr/local && \
    mv /usr/local/hadoop-${HADOOP_VERSION} ${HADOOP_HOME} && \
    rm hadoop-${HADOOP_VERSION}.tar.gz

# Update PATH
ENV PATH=$PATH:${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin

# Copy initialization script and set permissions
COPY ./hadoop-init.sh /hadoop-init.sh
RUN chmod +x /hadoop-init.sh

# Set entrypoint
ENTRYPOINT ["/hadoop-init.sh"]
