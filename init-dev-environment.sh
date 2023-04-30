#!/bin/bash

ID=$(docker ps | grep ais-web | awk '{ print $1 }')

if [ -z "$ID" ]
then
	echo 1>&2 "$0: Could not find the ais-web container. Is AIS running?"
	exit 2
fi

docker exec -it $ID python manage.py migrate --settings=local_settings
docker exec -it $ID python manage.py createsuperuser