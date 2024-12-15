# Frontend Service

## Introduction
The Frontend Service for the "Wikipedia Articles Summarization and Conversion to Audio" project provides a user interface that allows users to interact with the summarization system. This service is crucial for submitting requests for article summarization and receiving both textual summaries and audio playback directly in the web browser.

## Setup Instructions

### Prerequisites
- A Google Cloud Platform (GCP) account with billing enabled.
- Access to Google Compute Engine with permissions to create VM instances and set firewall rules.

### Configuration and Deployment
Before deploying the frontend, ensure the external IP addresses for service endpoints in the script files are correctly updated to match your environment.

#### 1. Virtual Machine Setup
Create a Virtual Machine (VM) instance in Google Cloud Compute Engine to host the frontend service. After creation, note the external IP address of this VM.

#### 2. Update JavaScript File
Modify the `script.js` to update endpoints with the external IP address of the ingress. This step ensures the frontend can correctly communicate with the backend services.

#### 3. Deploying the Frontend
Transfer the frontend files (HTML, CSS, JavaScript, and images) to the VM and configure the web server (Nginx) to serve these files.

## Modifications
- **File Paths and IP Addresses**: Review and adjust the paths in the commands and scripts to align with your GCP settings and local directory structure.
- **IP Address Update**: Replace the placeholder IP addresses in the `script.js` file with the actual external IP address of your ingress to ensure correct service interaction.

### Using the Scripts
To deploy the Frontend Service, execute the following scripts step-by-step:

1. **Creating a VM and Setting Up Firewall Rules**:
   Navigate to the directory containing `frontend1.sh` and execute the script to create a VM and configure firewall rules:
   ```bash
   ./frontend1.sh
   ```
   Ensure the script has execution permissions:
   ```bash
   chmod +x frontend1.sh
   ```

2. **Transferring Files and Configuring the Web Server**:
   After updating the JavaScript file, use `frontend2.sh` to transfer all frontend files to the VM and configure the Nginx web server:
   ```bash
   ./frontend2.sh
   ```
   Ensure the script has execution permissions:
   ```bash
   chmod +x frontend2.sh
   ```

### Testing the Service
To ensure that the Frontend Service is functioning correctly, access the external IP address of the VM using a web browser. The interface should load, and you should be able to interact with all provided features, including submitting requests and playing back audio summaries.

## Conclusion
The Frontend Service plays a pivotal role in the "Wikipedia Articles Summarization and Conversion to Audio" project by providing a direct way for users to interact with the summarization system. Proper setup and configuration are essential to ensure a seamless and responsive user experience.
