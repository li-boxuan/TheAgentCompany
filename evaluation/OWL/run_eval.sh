#!/bin/bash

# Check if tasks.txt exists
if [ ! -f "tasks.txt" ]; then
    echo "Error: tasks.txt file not found"
    exit 1
fi

# Read each line from tasks.txt
while IFS= read -r TASK_NAME || [ -n "$TASK_NAME" ]; do
    # Skip empty lines
    if [ -z "$TASK_NAME" ]; then
        continue
    fi
    
    echo "Processing task: $TASK_NAME"
    
    # Pull the Docker image
    echo "Pulling Docker image for $TASK_NAME..."
    sudo docker pull ghcr.io/li-boxuan/${TASK_NAME}-owl-image:latest
    
    # Create the results directory
    echo "Creating results directory for $TASK_NAME..."
    mkdir -p ./results/${TASK_NAME}
    
    # Run the Docker container
    echo "Running Docker container for $TASK_NAME..."
    sudo docker run --name ${TASK_NAME} --network host -v ./results/${TASK_NAME}:/host_output \
        --env-file .env ghcr.io/li-boxuan/${TASK_NAME}-owl-image:latest /bin/bash -c \
        "wget -O run_script.sh https://raw.githubusercontent.com/li-boxuan/owl/gaia58.18-on-tac/owl/run_theagentcompany.sh && \
        chmod +x run_script.sh && \
        ./run_script.sh && \
        cp -r ./owl/output/* /host_output/"
    
    # Clean up
    echo "Cleaning up for $TASK_NAME..."
    docker image rm ghcr.io/li-boxuan/${TASK_NAME}-owl-image
    docker system prune -f
    
    echo "Completed task: $TASK_NAME"
    echo "----------------------------------------"
    
done < "tasks.txt"

echo "All tasks completed"