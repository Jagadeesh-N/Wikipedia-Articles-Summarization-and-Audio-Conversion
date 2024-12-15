# Summarization Service

## Introduction
The Summarization Service within the "Wikipedia Articles Summarization and Conversion to Audio" project utilizes advanced Natural Language Processing (NLP) to extract and condense the core content of Wikipedia articles. This service significantly reduces the time users spend reading while providing a comprehensive understanding of the articles in a fraction of the original length.

## Setup Instructions

### Prerequisites
- Google Cloud Platform (GCP) account with billing enabled.
- Configured `kubectl` command-line tool with access to your Kubernetes cluster.
- Kubernetes cluster operational within your GCP environment.

### Configuration and Deployment
Please make the changes mentioned below as noted in the respective `.sh` file.

#### 1. Building and Pushing the Docker Image
Construct the Docker image for the summarization service and push it to your Google Container Registry.
*Note: Adjust the `Makefile` paths according to your project directory.*

#### 2. Deploying Summarization Service to Kubernetes
Deploy the service using Kubernetes deployment configurations to manage the service at scale.
*Note: Modify the file paths in the deployment command to align with your local environment.*

## Modifications
- **Project and Container Paths**: Ensure that paths and identifiers in the Docker commands and Kubernetes configurations reflect your actual GCP setup and directory structure.

### Using the Script
To deploy the Summarization Service, navigate to the directory containing `summarizer.sh` and execute the script:
```bash
./summarizer.sh
```
Make sure the script has execution permissions:
```bash
chmod +x summarizer.sh
```

### Testing the Service
To confirm that the Summarization Service is operating correctly, perform a test using port-forwarding and curl to interact with the service's health check endpoint.

1. **Port-forwarding**:
   Use kubectl to forward a local port to the service:
   ```bash
   kubectl port-forward deployment/summarizer-deployment 5000:5000
   ```

2. **Testing with Curl**:
   Send a request to the service’s health endpoint to verify its status:
   ```bash
   curl http://localhost:5000/health
   ```

If the service is correctly set up and running, you will receive a status indicating "healthy".

## Conclusion
The Summarization Service plays a crucial role in processing textual content, offering an efficient way to understand complex articles quickly. By integrating sophisticated NLP tools, this service ensures that users receive concise, accurate summaries, enhancing the accessibility and usability of information derived from Wikipedia.
