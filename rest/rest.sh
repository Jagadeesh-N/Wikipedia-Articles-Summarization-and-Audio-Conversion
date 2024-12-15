#!/bin/bash
########### Creating rest Service in kubernetes cluster ##############
make -C /home/jana3207/finalproject-final-project-team-61/rest build
make -C /home/jana3207/finalproject-final-project-team-61/rest push
kubectl apply -f /home/jana3207/finalproject-final-project-team-61/rest/rest-backend.yaml
kubectl apply -f /home/jana3207/finalproject-final-project-team-61/rest/rest-deployment.yaml
kubectl apply -f /home/jana3207/finalproject-final-project-team-61/rest/rest-ingress.yaml
echo "Rest service deployed successfully."