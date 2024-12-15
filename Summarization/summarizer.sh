#!/bin/bash
########### Creating Summarization Service in kubernetes cluster ##########
#1. Creating pods for summarization service using following commands
make -C /home/jana3207/finalproject-final-project-team-61/Summarization build
make -C /home/jana3207/finalproject-final-project-team-61/Summarization push
kubectl apply -f /home/jana3207/finalproject-final-project-team-61/Summarization/summarization-deployment.yaml
echo "Summarization service deployed successfully."