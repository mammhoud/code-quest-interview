#!/usr/bin/zsh
# # sudo docker stop $(sudo docker ps -aq)
# # sudo docker rm $(sudo docker ps -aq)
# # sudo docker rmi $(sudo docker images -q)
# Remove all docker volumes
# # sudo docker volume rm $(sudo docker volume ls -q)
# Pull the latest changes from the repository
# sudo git pull -f
rv run manage.py makemigrations
uv run manage.py migrate
# Activate the virtual environment again and collect static files
uv run manage.py collectstatic --no-input
# Start the docker containers with rebuild and remove orphans
sudo docker-compose up --build --remove-orphans -d
# Show the logs of the running containers

sudo docker-compose logs -f
# sudo docker-compose logs -f --tail=100