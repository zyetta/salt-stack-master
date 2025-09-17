# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /opt/salt

# Install system packages needed to build Salt
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git build-essential python3-dev libffi-dev libssl-dev libzmq3-dev \
        && rm -rf /var/lib/apt/lists/*

# Copy Salt submodule into container
COPY salt/ ./salt

RUN pip install --no-cache-dir -r salt/requirements/zeromq.txt

# Install Salt itself from the submodule so CLI scripts are available
RUN pip install --no-cache-dir ./salt

# Expose Salt Master ports
EXPOSE 4505 4506

# Start Salt Master
CMD ["salt-master", "-l", "info"]