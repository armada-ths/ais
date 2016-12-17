#!/bin/bash
/bin/bash -c "
    . /home/deployment/ais_venv/bin/activate;
    cd ~/ais;
    uwsgi --ini ais_uwsgi.ini
"
