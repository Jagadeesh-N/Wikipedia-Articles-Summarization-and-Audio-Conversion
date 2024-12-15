#!/bin/bash

### Deletion Commands for Google Cloud Resources ###

# 1. Deletion command for the created virtual machine instance
echo "Deleting Virtual Machine instance..."
gcloud compute instances delete frontend-vm --zone=us-central1-a

# 2. Deletion command for the Kubernetes cluster
echo "Deleting Kubernetes cluster..."
gcloud container clusters delete wikipedia-cluster --zone us-central1-a

# 3. Deletion commands for the storage bucket
echo "Deleting Storage Bucket..."
gsutil rm -r gs://wikipedia-summarizer-storage

# 4. Deletion commands for BigQuery dataset and table
echo "Deleting BigQuery dataset and table..."
bq rm -f -t wikipedia_summarizer_dataset.wikipedia_summarizer_table
bq rm -f -d wikipedia_summarizer_dataset

# 5. Deletion commands for container images in Google Container Registry (GCR)
echo "Deleting Container Images from GCR..."
gcloud container images delete gcr.io/dcsc2024-437804/wikipedia-summarizer-image --force-delete-tags

echo "All resources deleted successfully."