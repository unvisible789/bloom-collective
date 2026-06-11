FROM mcr.microsoft.com/devcontainers/python:3.11

# Install additional tools if needed
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends git curl \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install useful Python tools
RUN pip install --upgrade pip \
    && pip install black pytest mypy

# Set working directory
WORKDIR /workspaces/bloom-collective
