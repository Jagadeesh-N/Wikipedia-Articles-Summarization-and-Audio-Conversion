FROM python:3.8-slim

# Working directory
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir flask flask-cors redis requests

# Copy application files
COPY rest.py .

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "rest.py"]
