#!/bin/bash

PID=cat '/home/deployment/ais-master.pid'
kill -HUP $PID
