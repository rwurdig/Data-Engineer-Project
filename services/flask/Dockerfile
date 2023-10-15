# Use a more specific base image with Python 3.9
FROM python:3.9-alpine

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LDFLAGS="-L/usr/local/opt/openssl/lib"

# Install system dependencies
RUN apk update && \
    apk add --no-cache postgresql-dev gcc python3-dev musl-dev && \
    rm -rf /var/cache/apk/*

# Upgrade pip and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Show the app directory contents (for debugging)
RUN ls -la /usr/src/app/

# Use an entrypoint script to run commands
ENTRYPOINT ["sh", "app/docker-entrypoint.sh"]
