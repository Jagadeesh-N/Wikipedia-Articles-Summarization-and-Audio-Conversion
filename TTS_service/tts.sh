#!/bin/bash
########### Creating TTS Service in kubernetes cluster ##############
#1. Creating pods for tts service using following commands
make -C /home/jana3207/finalproject-final-project-team-61/TTS_service build
make -C /home/jana3207/finalproject-final-project-team-61/TTS_service push
kubectl apply -f /home/jana3207/finalproject-final-project-team-61/TTS_service/tts_service-deployment.yaml

echo "TTS service deployed successfully."