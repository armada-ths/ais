#!/bin/bash

PID=cat '/tmp/ais-master.pid'
kill -HUP $PID
