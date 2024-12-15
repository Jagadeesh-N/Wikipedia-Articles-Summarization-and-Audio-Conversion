# Base image for Python
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir flask google-cloud-bigquery pandas google-cloud-bigquery-storage

# Copy application files
COPY Database.py .
COPY wikipedia-service-account-key.json /app/wikipedia-service-account-key.json

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/wikipedia-service-account-key.json

# Run the application
CMD ["python", "Database.py"]
