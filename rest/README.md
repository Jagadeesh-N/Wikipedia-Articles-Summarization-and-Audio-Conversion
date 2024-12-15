# REST API Service

## Introduction
The REST API Service in the "Wikipedia Articles Summarization and Conversion to Audio" project functions as the interface between the frontend and various backend services. It orchestrates processes such as article retrieval, summarization, text-to-speech conversion, and metadata storage, ensuring seamless interaction across services.

## Setup Instructions

### Prerequisites
- Google Cloud Platform (GCP) account with billing enabled.
- Configured `kubectl` command-line tool with access to your Kubernetes cluster.
- Google Cloud SDK (`gcloud`) installed and configured on your machine.
- An operational Virtual Machine instance on Google Cloud Compute Engine with a static external IP address.

### Configuration and Deployment
Please make the changes mentioned below as noted in the respective `.sh` file.

#### 1. Virtual Machine Setup
Before deploying the REST API service, create a Virtual Machine (VM) instance in Google Cloud Compute Engine using the shell script in frontend directory`frontend1.sh`. Obtain the external IP address of this VM and update the `CORS` configuration and response headers in the `rest.py` file to match this IP.

#### 2. Building and Pushing the Docker Image
Compile the Docker image for the REST API service and push it to your Google Container Registry.
*Note: Adjust the `Makefile` paths to reflect your project directory.*

#### 3. Deploying REST API Service to Kubernetes
Deploy the service using Kubernetes deployment configurations to manage the service efficiently at scale.
*Note: Ensure file paths in the deployment commands correspond with your local environment setup.*

## Modifications
- **File Paths and Project Settings**: Check and modify any project-specific paths and settings in the Docker commands, Kubernetes configurations, and `.sh` script to reflect your actual GCP and local directory structure.
- **IP Address Replacement**: Replace the placeholder IP address in the `rest.py` file's CORS settings and response headers with the external IP address of your VM to ensure proper functioning of cross-origin requests.

### Using the Script
1. **Creating a VM and Setting Up Firewall Rules**:
   Navigate to the frontend directory containing `frontend1.sh` and execute the script to create a VM and configure firewall rules:
   ```bash
   ./frontend1.sh
   ```
   Ensure the script has execution permissions:
   ```bash
   chmod +x frontend1.sh
   ```
2. **Later deploy the REST API Service**, navigate to the directory containing `rest.sh` and execute the script:
   ```bash
   ./rest.sh
   ```
   Ensure the script has execution permissions:
   ```bash
   chmod +x rest.sh
   ```

### Testing the Service
To verify that the REST API Service is fully operational, perform a test using port-forwarding and curl to interact with the service's health check endpoint.

1. **Port-forwarding**:
   Use kubectl to forward a local port to the service:
   ```bash
   kubectl port-forward deployment/rest-api-deployment 5000:5000
   ```

2. **Testing with Curl**:
   Send a request to the service’s health endpoint to check its status:
   ```bash
   curl http://localhost:5000/health
   ```

If the service is correctly set up and running, you will receive a status indicating "healthy".

## Conclusion
The REST API Service is critical for facilitating communication between the frontend and the various backend services. By properly setting up this service, you ensure that user requests are efficiently processed and that the system operates seamlessly, enhancing the overall user experience of the "Wikipedia Articles Summarization and Conversion to Audio" project.
