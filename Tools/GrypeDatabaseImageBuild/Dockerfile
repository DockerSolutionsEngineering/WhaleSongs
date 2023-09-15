# Use a Debian base image
FROM debian:bullseye-slim

# Label the image with metadata
LABEL maintainer="Jay Schmidt <jay.schmidt@docker.com>"
LABEL description="Build a grype image with a custom DB"

# Install necessary packages in one layer to reduce image size
RUN apt-get update && \
    apt-get install -y \
    curl \
    bash \
    jq \
    python3-pip && \
    # Clean up to reduce image size
    rm -rf /var/lib/apt/lists/*

# Install grype using the official installation script
RUN curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin

# Install grype-db using the official installation script
RUN curl -sSfL https://raw.githubusercontent.com/anchore/grype-db/main/install.sh | sh -s -- -b /usr/local/bin

# Install Vunnel using pip
RUN pip install vunnel

# Set up the environment for grype by creating necessary directories
RUN mkdir -p ./grype/db

# Copy the grype and grype-db configuration files from the host to the image
# and rename them to start with a dot, making them hidden files
COPY grype.yaml /root/.grype.yaml
COPY grype-db.yaml /root/.grype-db.yaml

# Set the working directory to /root to avoid using absolute paths
WORKDIR /root

# Run the grype-db commands to set up the database with verbose logging
# and import the generated database archive (the wildcard '*' handles changing filenames)
RUN grype-db -vv -g -p alpine && \
    grype-db -vv -g -p alpine build && \
    grype db import ./build/*.tar.gz

# Set the entry point to grype so that the container runs grype by default
ENTRYPOINT ["grype"]
