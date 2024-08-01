#!/bin/bash

# This script will execute the makemigrations script inside
# the ais-web docker container, given it's up and running.

# Usage: ./make-migration <name of migration> <name of module where field was added>
# or ./make-migration.sh <name of migration> <name of module where field was added>

if [ $# -lt 2 ]; then
	echo 1>&2 "usage: $0 <name of migration> <name of module where field was added>"
	exit 2
fi

ID=$(docker ps | grep ais-web | awk '{ print $1 }')

if [ -z "$ID" ]
then
	echo 1>&2 "$0: Could not find the ais-web container. Is AIS running?"
	exit 2
fi

docker exec -it $ID python manage.py makemigrations --name $1 $2 --settings=local_settings