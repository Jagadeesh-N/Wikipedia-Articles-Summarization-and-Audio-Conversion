#!/bin/bash
######### Creating a VM for frontend ################
#1. Create a VM
gcloud compute instances create frontend-vm \
    --machine-type=e2-medium \
    --image-family=debian-11 \
    --image-project=debian-cloud \
    --zone=us-central1-a \
    --tags=frontend-http \
    --scopes=https://www.googleapis.com/auth/cloud-platform
    
#2. Creating a Firewall:

gcloud compute firewall-rules create allow-http-frontend \
    --direction=INGRESS \
    --priority=1000 \
    --network=default \
    --action=ALLOW \
    --rules=tcp:80 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=frontend-http