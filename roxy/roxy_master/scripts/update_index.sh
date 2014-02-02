#!/bin/bash

cd /var/www/Roxy-Proxy
source venv/bin/activate

cd /var/www/Roxy-Proxy/roxy
./manage.py update_index

