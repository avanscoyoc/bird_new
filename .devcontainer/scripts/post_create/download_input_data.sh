#/bin/bash

Check if input data directory exists

if [ ! -d "/workspaces/bird_new/data" ]; then

    # Create input data directory

    mkdir -p /workspaces/bird_new/data

    # Download the data, shared as public links from Google Cloud Storage Bucket

    echo "Downloading input data..."

    wget -O /workspaces/bird_new/data/non-avian_ML.zip https://storage.cloud.google.com/dse-staff/audio/non-avian_ML.zip   
    
    # Unzip the downloaded file
    unzip /workspaces/bird_new/data/non-avian_ML.zip -d /workspaces/bird_new/data

    # Remove the zip file after extraction
    rm /workspaces/bird_new/data/non-avian_ML.zip
fi