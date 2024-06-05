# toothWave

docker rmi -f $(docker ps -aq)
docker rmi -f $(docker images -aq)
docker volume rm $(docker volume ls -q)

# Build steps in prod

docker-compose -f docker-compose.prod.yml up --build
docker-compose -f docker-compose.prod.yml up -d
