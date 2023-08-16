#!/bin/bash

ID=$(docker ps | grep ais-web | awk '{ print $1 }')

if [ -z "$ID" ]
then
	echo 1>&2 "$0: Could not find the ais-web container. Is AIS running?"
	exit 2
fi

echo "Migrating database to latest state ..." &&
docker exec -it $ID python manage.py migrate --settings=local_settings &&
echo "... done migrating database to latest state"

echo "Create super user (optional, press ctrl+c to skip) ..." &&
docker exec -it $ID python manage.py createsuperuser &&
echo "... done creating super user. You are all setup!"