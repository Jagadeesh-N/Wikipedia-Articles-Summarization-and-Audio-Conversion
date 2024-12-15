# Base image for Python
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y ffmpeg && \
    pip install --no-cache-dir gtts pydub flask && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the TTS script
COPY tts_service.py .

# Run the script
CMD ["python", "tts_service.py"]
