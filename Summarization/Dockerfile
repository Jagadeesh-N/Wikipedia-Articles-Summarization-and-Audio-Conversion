# Base image for Python
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir requests beautifulsoup4 transformers torch flask

# Copy the summarization script
COPY summarizer.py .

# Expose the port
EXPOSE 5000

# Run the script
CMD ["python", "summarizer.py"]