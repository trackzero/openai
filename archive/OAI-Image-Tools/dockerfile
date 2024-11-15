# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory to /app
WORKDIR /app

COPY requirements.txt .

# Install ffmpeg and other system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 && \
    rm -rf /var/lib/apt/lists/*

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 5050
EXPOSE 5050

# Define environment variables (set these in the container)
ENV OPENAI_API_KEY=your_openai_api_key
ENV FLASK_SECRET_KEY=your_flask_secret_key

# Start your Flask app
CMD ["python", "app.py"]
