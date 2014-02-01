Roxy Proxy
===========

Steps:

1. Check out Roxy-Master GitHub repository.

2. Set up virtualenv environment.

3. pip install -r roxy/roxy_master/requirements.pip

4. Set up Postgres database:

    postgres=# CREATE USER roxy WITH PASSWORD 'roxyproxy';
    CREATE ROLE
    postgres=# CREATE DATABASE roxyproxy;
    CREATE DATABASE
    postgres=# GRANT ALL PRIVILEGES ON DATABASE roxyproxy TO roxy;
    GRANT

5. cd roxy_master; ./manage.py syncdb; ./manage.py migrate; ./manage.py collectstatic

6. Update the local Apache WSGI configuration to point to Django install & venv. Relevant lines:

    WSGIPythonPath /var/www/django/venv/lib/python2.7/site-packages:/var/www/django/roxy
	
    WSGIScriptAlias / /var/www/django/roxy/roxy_master/wsgi.py
    Alias /static /var/www/django/roxy/static
    Alias /media /var/www/django/roxy/media

7. Update default Django site from pointing to example.com to point to server's hostname.
	
8. From the Django admin, add an Auth > Group object called "Users". Add User Profiles > Group Profile and set the proxy duration.
	
9. Check out Roxy-Proxy-Server repository.

10. Install requirements: pip install -r requirements.pip

11. Setup Twisted proxy server:

    roxy.tac (port number):
    roxy_proxy = internet.TCPServer(8080, roxy_factory)

    roxy/roxy.py (pointer to master Django controller):
    PROXY_MASTER = 'ec2-54-221-7-65.compute-1.amazonaws.com'

12. Test proxy setup: twistd -ny roxy.tac

13. In Django, add Proxy > Proxy Server object pointing to Twisted proxy server.

14. Test Django-Twisted connection by visiting http://<host>/proxy/proxy_test. Note that this test may falsely fail in cases where the server has separate internal and external IP addresses (Amazon EC2). Check the twisted.log file in these cases.

15. Verify that content/management/commands/fetch_content.py points to the right place to copy content to catalog. Check local paths in  content/management/commands/catalog_content.py, as well.

16. Set up Solr with Django Haystack 2.1.0:

	http://django-haystack.readthedocs.org/en/v2.1.0/
	
17. Once Solr & Haystack are up and running, add update.sh to the local crontab.
