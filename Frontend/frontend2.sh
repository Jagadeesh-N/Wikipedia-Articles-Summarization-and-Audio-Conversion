#!/bin/bash
#3. Forwarding all files into VM  using following command:
gcloud compute scp /home/jana3207/finalproject-final-project-team-61/Frontend/index.html /home/jana3207/finalproject-final-project-team-61/Frontend/script.js /home/jana3207/finalproject-final-project-team-61/Frontend/style.css /home/jana3207/finalproject-final-project-team-61/Frontend/Wikipedia-2.jpeg frontend-vm:~/ --zone=us-central1-a

#4. SSH into VM
gcloud compute ssh frontend-vm --zone=us-central1-a --command="sudo apt update && sudo apt install -y nginx && sudo mv ~/index.html ~/script.js ~/style.css ~/Wikipedia-2.jpeg /var/www/html/ && sudo chmod -R 755 /var/www/html/ && sudo chown -R www-data:www-data /var/www/html/ && sudo systemctl restart nginx"