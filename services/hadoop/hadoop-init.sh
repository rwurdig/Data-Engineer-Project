#!/bin/bash

# Initialize variables
DATANODE_HOST="hadoop-datanode"
DATANODE_PORT=9864
MAX_RETRIES=20
SLEEP_INTERVAL=3

# Function to check if the datanode is up
check_datanode() {
  nc -z "$DATANODE_HOST" "$DATANODE_PORT"
}

# Main function to wait for the datanode
wait_for_datanode() {
  local retries=0
  while ! check_datanode; do
    retries=$((retries + 1))
    if [ $retries -ge $MAX_RETRIES ]; then
      >&2 echo "Datanode is unavailable - reached max retries. Exiting."
      exit 1
    fi
    >&2 echo "Datanode is unavailable - sleeping for $SLEEP_INTERVAL seconds."
    sleep "$SLEEP_INTERVAL"
  done
  echo "Datanode is up."
}

# Execute the main function
wait_for_datanode
