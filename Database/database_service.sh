#!/bin/bash
###### Creating Database Serbice in kubernetes Cluster #########
# 1. Enable bigquery api 
gcloud services enable bigquery.googleapis.com

# 2. Creating a dataset in big query:
bq --location=us-central1 mk -d \
	--description "Dataset for Wikipedia Summarizer Project" \
	wikipedia_summarizer_dataset
	
# 3. creating a table in big query
bq mk --table \
--schema=/home/jana3207/finalproject-final-project-team-61/Database/schema.json \
wikipedia_summarizer_dataset.wikipedia_summarizer_table


# 4. Creating a secret for bigquery in kubernetes cluster:
kubectl create secret generic bigquery-service-account-secret \
 --from-file=wikipedia-service-account-key.json=/home/jana3207/finalproject-final-project-team-61/Database/wikipedia-service-account-key.json
 
#5. Creating pods in kubernetes cluster for Database service using the following commands
make -C /home/jana3207/finalproject-final-project-team-61/Database build
make -C /home/jana3207/finalproject-final-project-team-61/Database push
kubectl apply -f /home/jana3207/finalproject-final-project-team-61/Database/Database-deployment.yaml

echo "Database service deployed successfully."