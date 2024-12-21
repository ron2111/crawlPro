#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python -m venv venv
fi

# Activate virtual environment
source venv/Scripts/activate

# Install requirements
pip install -r requirements.txt

# Run crawler with example domains
python src/main.py --domains amazon.com myntra.com flipkart.com
