#!/bin/bash
while read line           
do           
    kill -HUP line           
done </home/deployment/ais-master.pid 

