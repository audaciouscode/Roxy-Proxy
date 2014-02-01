#!/bin/bash

cd /var/www/roxy_content
source venv/bin/activate

cd /var/www/roxy_content/roxy_master
./manage.py update_index

