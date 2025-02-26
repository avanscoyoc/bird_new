#!/bin/bash

# Ensure unzip is installed
if ! command -v unzip &> /dev/null; then
    echo "Installing unzip..."
    sudo apt update && sudo apt install -y unzip
fi

# Check if the directory exists
if [ ! -d "/workspaces/bird_new/data" ]; then
    mkdir -p /workspaces/bird_new/data
fi

# Download data if not already present
if [ ! -f "/workspaces/bird_new/data/non-avian_ML.zip" ]; then
    echo "Downloading input data..."
    curl -L -o /workspaces/bird_new/data/non-avian_ML.zip "https://storage.googleapis.com/dse-staff-public/non-avian_ML.zip"
fi

# Verify download before unzipping
if [ -f "/workspaces/bird_new/data/non-avian_ML.zip" ]; then
    echo "Unzipping data..."
    unzip -o /workspaces/bird_new/data/non-avian_ML.zip -d /workspaces/bird_new/data/
    rm /workspaces/bird_new/data/non-avian_ML.zip
    echo "Data extraction complete!"
else
    echo "Download failed. File not found!"
    exit 1
fi
