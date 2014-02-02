#!/bin/bash

cd /var/www/Roxy-Proxy
source venv/bin/activate
cd roxy

# ./manage.py fetch_content ubuntu@logging.roxyproxy.org:roxy_proxy/twisted/content
./manage.py fetch_content /var/www/Roxy-Proxy/proxy/content
./manage.py catalog_content
./manage.py history_report
./manage.py top_domains_report
./manage.py update_index

