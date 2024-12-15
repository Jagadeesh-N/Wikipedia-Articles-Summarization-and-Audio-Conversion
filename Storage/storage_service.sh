#!/bin/bash
####### Creating Storage Service in kubernetes Cluster ########
# 1. Creating a storage bucket
gcloud storage buckets create gs://wikipedia-summarizer-storage \
	--location=us-central1 \
	--default-storage-class=STANDARD
	
#2. Add policy to that bucket :
gcloud storage buckets add-iam-policy-binding gs://wikipedia-summarizer-storage \
	--member="serviceAccount:wikipedia-service-account@dcsc2024-437804.iam.gserviceaccount.com" \
	--role="roles/storage.objectAdmin"
	
# 3. Creating a secret key for storage in kubernetes cluster:
kubectl create secret generic wikipedia-latest-account-key \
	--from-file=wikipedia-service-account-key.json=/home/jana3207/finalproject-final-project-team-61/Storage/wikipedia-service-account-key.json

#4. Creating pods in kubernetes cluster using the following commands
make -C /home/jana3207/finalproject-final-project-team-61/Storage build
make -C /home/jana3207/finalproject-final-project-team-61/Storage push
kubectl apply -f /home/jana3207/finalproject-final-project-team-61/Storage/storage-deployment.yaml

echo "Storage service deployed successfully."