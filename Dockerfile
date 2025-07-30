# Use the official Python base image
FROM python:3.10.6

# Set a working directory inside the container
WORKDIR /app

# Copy your app code and requirements into the container
COPY package_folder/ package_folder/
COPY models/ models/
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 8000

# Start the FastAPI server
MD ["uvicorn", "package_folder.api_fileC:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

#CMD uvicorn package_folder.api_file:app --host 0.0.0.0 --port $PORT -
#lecture said this command was supposed to be used to deploy the container
#local comand didn't have the port part
