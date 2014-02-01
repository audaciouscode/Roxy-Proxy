#!/bin/bash

cd /var/www/roxy_content
source venv/bin/activate

cd /var/www/roxy_content/roxy_content
./manage.py catalog_content

