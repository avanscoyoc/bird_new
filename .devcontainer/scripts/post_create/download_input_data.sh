#/bin/bash

# Check if input data directory exists
if [ ! -d "/workspaces/bird_new/data" ]; then

    # Create input data directory
    mkdir -p /workspaces/bird_new/data

    # Download the data, shared as public links from Google Cloud Storage Bucket
    echo "Downloading input data..."
    wget -O /workspaces/bird_new/data/audio https://console.cloud.google.com/storage/browser/dse-staff/audio    #FIXME: Add path to google cloud storage bucket
   
fi