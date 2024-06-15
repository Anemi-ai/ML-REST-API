# Using base image Python version 3.12 slim
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Copy requirements.txt to install Python dependencies
COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --upgrade pip --no-cache-dir -r requirements.txt

# Copy entire current directory contents into the container at /app
COPY . .

# Expose port 8080 for the Flask app
EXPOSE 8080

# Command to run Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
