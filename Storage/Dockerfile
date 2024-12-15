# Base image for Python
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir google-cloud-storage flask requests

# Copy the storage script
COPY storage.py .

# Copy the service account key into the container (replace with your local key path)
COPY wikipedia-service-account-key.json /app/wikipedia-service-account-key.json
# Set environment variable for service account key
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/wikipedia-service-account-key.json

# Expose the port
EXPOSE 5000

# Run the application
CMD ["python", "storage.py"]
