#!/bin/bash

###### Initial Setup #############
# 1. Setting up Project ID -- Change your respective project id.
gcloud config set project dcsc2024-437804

# 2. Enabling apis for project
gcloud services enable \
        compute.googleapis.com \
        container.googleapis.com \
        pubsub.googleapis.com \
        storage.googleapis.com \
        sqladmin.googleapis.com \
        redis.googleapis.com \
        iam.googleapis.com \
        containerregistry.googleapis.com
    
# # 3. Creating a service account 
# gcloud iam service-accounts create wikipedia-service-account \
#     --description="Service account for Wikipedia summarization project" \
#     --display-name="Wikipedia Service Account"
    
# # 4. Assigning Roles/Permissions for Service Account - please do check the project id before executing the commands

# gcloud projects add-iam-policy-binding dcsc2024-437804 \
#     --member="serviceAccount:wikipedia-service-account@dcsc2024-437804.iam.gserviceaccount.com" \
#     --role="roles/storage.admin"
# gcloud projects add-iam-policy-binding dcsc2024-437804 \
#     --member="serviceAccount:wikipedia-service-account@dcsc2024-437804.iam.gserviceaccount.com" \
#     --role="roles/pubsub.editor"
# gcloud projects add-iam-policy-binding dcsc2024-437804 \
#     --member="serviceAccount:wikipedia-service-account@dcsc2024-437804.iam.gserviceaccount.com" \
#     --role="roles/container.admin"
# gcloud projects add-iam-policy-binding dcsc2024-437804 \
#     --member="serviceAccount:wikipedia-service-account@dcsc2024-437804.iam.gserviceaccount.com" \
#     --role="roles/cloudsql.admin"
# gcloud projects add-iam-policy-binding dcsc2024-437804 \
#     --member="serviceAccount:wikipedia-service-account@dcsc2024-437804.iam.gserviceaccount.com" \
#     --role="roles/redis.admin"
# gcloud projects add-iam-policy-binding dcsc2024-437804 \
#     --member="serviceAccount:wikipedia-service-account@dcsc2024-437804.iam.gserviceaccount.com" \
#     --role="roles/bigquery.dataEditor"
    
# gcloud projects add-iam-policy-binding dcsc2024-437804 \
#     --member="serviceAccount:wikipedia-service-account@dcsc2024-437804.iam.gserviceaccount.com" \
#     --role="roles/bigquery.user"
    
# # 5. Generating a Key for Service Account:
# gcloud iam service-accounts keys create ~/wikipedia-service-account-key.json \
#     --iam-account=wikipedia-service-account@dcsc2024-437804.iam.gserviceaccount.com
    
# # 6. Exporting :
# export GOOGLE_APPLICATION_CREDENTIALS=~/wikipedia-service-account-key.json

#7. Creating Kubernetes Cluster for the project :

gcloud container clusters create wikipedia-cluster \
    --num-nodes=2 \
    --zone=us-central1-a \
    --machine-type=e2-standard-4 \
    --enable-autoscaling \
    --min-nodes=2 \
    --max-nodes=3 \
    --enable-ip-alias \
    --release-channel=regular
    
#8. Storing Cluster Credentials :
gcloud container clusters get-credentials wikipedia-cluster --zone us-central1-a

# 9. Checking for the nodes in created cluster:
kubectl get nodes

# 10. Authenicate docker with GCR:
gcloud auth configure-docker

echo "Environment setup complete....till step 10 "