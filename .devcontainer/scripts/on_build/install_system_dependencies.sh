#!/bin/bash

# Install system dependencies
apt-get update && apt-get install -y \
     \                                  #FIXME: Add system dependencies here
    && rm -rf /var/lib/apt/lists/*