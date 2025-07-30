# Use the official Python base image
FROM python:3.10.6
#FROM python:3.10-slim

# Copy your app code and requirements into the container
COPY package_folder/ package_folder/
COPY models/ models/
COPY requirements.txt

# Install Python dependencies
RUN pip install -r requirements.txt

# Local
#CMD uvicorn package_folder.api_file:app --host 0.0.0.0

# Deployed
CMD uvicorn package_folder.api_file:app --host 0.0.0.0 --port $PORT

#lecture said this command was supposed to be used to deploy the container
#local comand didn't have the port part
