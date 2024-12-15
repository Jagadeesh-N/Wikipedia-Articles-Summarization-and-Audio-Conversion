# Redis Service

## Introduction
The Redis Service in the "Wikipedia Articles Summarization and Conversion to Audio" project functions as a high-speed data caching layer. By using Redis, this service significantly enhances the performance of data retrieval processes, crucial for delivering fast responses for recurring queries within the system.

## Setup Instructions

### Prerequisites
- Google Cloud Platform (GCP) account with billing enabled.
- Configured `kubectl` command-line tool with access to your Kubernetes cluster.
- Kubernetes cluster operational within your GCP environment.

### Configuration and Deployment
Please make the changes mentioned below as noted in the respective `.sh` file.

#### 1. Creating Redis Deployment and Service
Deploy Redis using the Kubernetes configuration that sets up both the deployment and the necessary service for Redis interaction.
*Note: Adjust the paths in the commands according to where your YAML files are stored.*

## Modifications
- **File Paths**: Adjust file paths in the script to match the directory structure on your machine where the necessary files are located, particularly for the deployment and service YAML files.

### Using the Script
To execute the setup for the Redis Service, navigate to the directory containing `redis.sh` and run the script:
```bash
./redis.sh
```
Ensure you have execution permissions set on the script:
```bash
chmod +x redis.sh
```

### Testing the Service
Verify that the Redis Service is operational by performing a simple connection test using port-forwarding and a Redis client tool such as `redis-cli`:

1. **Port-forwarding**:
   Use kubectl to forward a local port to the Redis service:
   ```bash
   kubectl port-forward deployment/redis-deployment 6379:6379
   ```

2. **Testing with Redis Client**:
   Connect using the Redis client:
   ```bash
   redis-cli -h localhost -p 6379
   ```
   You can then try a simple command like `PING` which should return `PONG` if the service is running properly.

This test confirms the connectivity and readiness of the Redis Service within your Kubernetes cluster.

## Conclusion
Once setup and tested, the Redis Service will enhance the performance of the system by caching frequently accessed data, thus reducing latency and improving the user experience. This service is essential for maintaining high throughput and responsiveness in the "Wikipedia Articles Summarization and Conversion to Audio" project.
