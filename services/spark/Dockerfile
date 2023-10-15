# Use a specific version for reproducibility
FROM bitnami/spark:3.2.1-debian-10-r98 as builder

# Set environment variables for better caching
ENV POSTGRES_JDBC_VERSION=42.3.5

# Download PostgreSQL JDBC driver and place it in the Spark jars directory
RUN curl -L -o /opt/bitnami/spark/jars/postgresql-${POSTGRES_JDBC_VERSION}.jar \
    https://jdbc.postgresql.org/download/postgresql-${POSTGRES_JDBC_VERSION}.jar

# Multi-stage build to keep the image size small
FROM bitnami/spark:3.2.1-debian-10-r98

# Copy only the necessary jar from the builder stage
COPY --from=builder /opt/bitnami/spark/jars/postgresql-*.jar /opt/bitnami/spark/jars/

# Additional configurations can be added here
# ...
