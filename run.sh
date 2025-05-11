#!/usr/bin/zsh

# Navigate to the BOTO-CRM directory
# cd BOTO-CRM/
# Activate the virtual environment
# source ../.venv/bin/activate
# Stop and remove all running containers and images
sudo docker stop $(sudo docker ps -aq)
sudo docker rm $(sudo docker ps -aq)
sudo docker rmi $(sudo docker images -q)
# Remove all docker volumes
sudo docker volume rm $(sudo docker volume ls -q)
# Pull the latest changes from the repository
# sudo git pull -f
python backend/manage.py migrate
# Activate the virtual environment again and collect static files
python backend/manage.py collectstatic --no-input
# Start the docker containers with rebuild and remove orphans
sudo docker-compose -f docker-compose.nginx.yml up --build --remove-orphans -d
# Show the logs of the running containers
sudo docker-compose -f docker-compose.nginx.yml logs -f