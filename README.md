# toothWave

docker rmi -f $(docker ps -aq)
docker rmi -f $(docker images -aq)
docker volume rm $(docker volume ls -q)

# Build steps in prod

docker-compose -f docker-compose.prod.yml up --build
docker-compose -f docker-compose.prod.yml up -d

## DATA BASE CREATE

CREATE USER crentist WITH PASSWORD tesca123;
ALTER ROLE crentist WITH LOGIN;
ALTER ROLE crentist SET client_encoding TO 'utf8';
ALTER ROLE crentist SET default_transaction_isolation TO 'read committed';
ALTER ROLE crentist SET timezone TO 'America/Mexico_City';
CREATE DATABASE dentapp;
\c dentapp;
CREATE SCHEMA dentapp;
GRANT ALL PRIVILEGES ON SCHEMA dentapp TO crentist;
DROP SCHEMA public;
GRANT ALL PRIVILEGES ON DATABASE dentapp TO crentist;
ALTER USER crentist WITH SUPERUSER;
sudo cp -r dist/\* /var/www/html/
