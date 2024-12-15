# TTS (Text-to-Speech) Service

## Introduction
The TTS (Text-to-Speech) Service in the "Wikipedia Articles Summarization and Conversion to Audio" project is responsible for converting text summaries into audible speech. This service enhances the accessibility of summarized content by providing auditory outputs that can be used by individuals with visual impairments or those who prefer audio learning.

## Setup Instructions

### Prerequisites
- Google Cloud Platform (GCP) account with billing enabled.
- Configured `kubectl` command-line tool with access to your Kubernetes cluster.
- Google Cloud SDK (`gcloud`) installed and configured on your machine.

### Configuration and Deployment
Please make the changes mentioned below as noted in the respective `.sh` file.

#### 1. Building and Pushing the Docker Image
Construct the Docker image for the TTS service and push it to your Google Container Registry.
*Note: Adjust the `Makefile` paths according to your project directory.*

#### 2. Deploying TTS Service to Kubernetes
Deploy the service using Kubernetes deployment configurations to manage the service at scale.
*Note: Modify the file paths in the deployment command to align with your local environment.*

## Modifications
- **Project and Container Paths**: Ensure that paths and identifiers in the Docker commands and Kubernetes configurations reflect your actual GCP setup and directory structure.

### Using the Script
To deploy the TTS Service, navigate to the directory containing `tts.sh` and execute the script:
```bash
./tts.sh
```
Make sure the script has execution permissions:
```bash
chmod +x tts.sh
```

### Testing the Service
To confirm that the TTS Service is operating correctly, perform a test using port-forwarding and curl to interact with the service's health check endpoint.

1. **Port-forwarding**:
   Use kubectl to forward a local port to the service:
   ```bash
   kubectl port-forward deployment/tts-deployment 5000:5000
   ```

2. **Testing with Curl**:
   Send a request to the service’s health endpoint to verify its status:
   ```bash
   curl http://localhost:5000/health
   ```

If the service is correctly set up and running, you will receive a status indicating "healthy".

## Conclusion
The TTS Service is integral to making summarized content more accessible through audio format. By converting text summaries into high-quality audio, this service fulfills the project's goal of enhancing information accessibility and catering to diverse user preferences.
