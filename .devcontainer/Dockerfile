# First, grab a Unix image with pixi installed
FROM python:3.10-bullseye

# Set the working directory
WORKDIR /workspaces/bird_new

# Run on build scripts (system dependencies)
COPY .devcontainer/scripts .devcontainer/scripts
RUN .devcontainer/scripts/run_on_build.sh

# Pip install requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt