#!/bin/bash

#docker build -t python/pestyle -f ./docker/Dockerfile .
#docker run -v /home/nv/2017_python/msite/pestyle/static:/var/www/static -v /home/nv/2017_python/msite:/var/www/sql/  -t -p 8080:8080 -p 22333:8000 python/pestyle
sudo apt-get update
sudo apt-get install wget
wget -qO- https://get.docker.com/ | sh
docker run -v /opt/project/2017_python/msite/pestyle/static:/var/www/static -v /opt/project/2017_python/msite/:/var/www/sql/  -t -p 80:80 glowlex/pestyle

#sudo docker exec -i -t  nifty_mestorf bash
#docker run -it -d 71f7beea52aa
#docker-compose build project
#docker-compose stop && docker-compose rm -f && docker-compose build --no-cache project && docker-compose up -d
#docker-compose run --rm --service-ports project
