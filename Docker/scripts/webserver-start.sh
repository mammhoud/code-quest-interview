#! /usr/bin/env sh
# exit on error
set -o errexit
set -e
echo "--> Starting webserver process ..."


cd /app

# hatch env show
# Install Modules, Webpack and Tailwind set up
# npm i
# npm run build
# npx tailwindcss -i ./static/assets/style.css -o ./static/dist/css/output.css # TODO Add another installation for other web packages

echo "--> Starting Nginx ..."
cp docker/nginx/default.conf /etc/nginx/conf.d/default.conf
cp docker/nginx/nginx.conf /etc/nginx/nginx.conf
echo "--> Nginx Starting with Docker ..."
echo "----------------------------"
nginx -t
echo "----------------------------"
# sh -c "hatch run docker:migrations" > logs/docker.migrations.log
# sh -c "hatch run docker:assets" > logs/docker.assets.log
echo "----------------------------"
echo "----------------------------"
nginx -e /app/logs/nginx.log -g "daemon on;"
echo "----------------------------"
echo "--> Nginx Started"

echo "--> Exposed port 8000 for django server"
echo "--> Exposed port 8880 for nginx web-server"
hatch run docker:run
