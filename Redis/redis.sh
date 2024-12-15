#!/bin/bash
########### Creating Redis Service in kubernetes cluster ##########
# 1.creating pods for redis service using following commands 
kubectl apply -f /home/jana3207/finalproject-final-project-team-61/Redis/redis-secret.yaml
kubectl apply -f /home/jana3207/finalproject-final-project-team-61/Redis/redis-deployment.yaml

echo "Redis service deployed successfully."