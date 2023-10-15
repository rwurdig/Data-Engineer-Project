import os
import multiprocessing

# Bind to 0.0.0.0 to make the service accessible from outside the container
bind = os.getenv("GUNICORN_BIND", "0.0.0.0:5000")

# Dynamically determine the number of workers based on CPU cores
workers = os.getenv("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1)

# Limit the number of requests a worker will process before restarting
max_requests = os.getenv("GUNICORN_MAX_REQUESTS", 1000)

# Use 'gevent' for better performance
worker_class = os.getenv("GUNICORN_WORKER_CLASS", "gevent")

# Logging configurations
accesslog = os.getenv("GUNICORN_ACCESS_LOG", "-")
errorlog = os.getenv("GUNICORN_ERROR_LOG", "-")
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")
