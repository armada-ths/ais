#!/bin/bash

docker compose up db 

docker exec -i ais_db_1 psql -U ais_dev < scripts/vagrant/ais-developer-database.sql

docker compose up web 
