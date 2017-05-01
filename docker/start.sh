sudo docker exec -i -t  nifty_mestorf bash
docker run -it -d 71f7beea52aa
docker-compose build project
docker-compose stop && docker-compose rm -f && docker-compose build --no-cache project && docker-compose up -d
docker-compose run --rm --service-ports project
