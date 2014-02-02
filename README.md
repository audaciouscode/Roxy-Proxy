Roxy Proxy
==========

Roxy Proxy is an HTTP (*not HTTPS*) proxy server that uses a Twisted HTTP proxy to route and store users' HTTP requests. A Django application directs users to the proxy server and provides a mechanism for retrieving content gathered from the proxy server and catalog & index it in a local Postgres database and Solr index server. Once cataloged and indexed, content from Roxy can be analyzed as desired.

Roxy associated gathered content with a user login, so the first time a user attempts to use Roxy, the system will prompt them for a login. This login is associated with a session, which is associated with teh captured content. Users can elect to choose a regular session, where all content is stored and cataloged, or a private session where the proxy server works as intended, but the system does not record the user's request activity.

Roxy is the creation of Ericka Menchen-Trevino and was developed by Chris Karr. It is provided under a GPLv3 open-source license.


Installation
============

_Note that this setup assumes some familiarity with Django, Postgres, Solr, and Twisted. If you're not comfortable with these packages, please learn how these software packages work before attempting to install Roxy._

Steps:

1. Install Apache, WSGI, Postgres, and Python's virtual-env.

2. Check out `Roxy-Proxy` repository.

3. Set up a `virtualenv` environment. Next to the `proxy` and `roxy` files works well.

4. Install Python requirements:

    ```pip install -r roxy/roxy_master/requirements.pip```
    
    Note that you may need to install some other system prerequisites (such as Postgres development headers) in order to complete this step successfully. This will vary by platform and each platform's installation defaults.

4. Set up Postgres database:

    ```
    postgres=# CREATE USER roxy WITH PASSWORD 'roxyproxy';
    CREATE ROLE
    postgres=# CREATE DATABASE roxyproxy;
    CREATE DATABASE
    postgres=# GRANT ALL PRIVILEGES ON DATABASE roxyproxy TO roxy;
    GRANT
    ```
    
5. Create & populate the Django database:
    ```
    cd roxy
    ./manage.py syncdb 
    ./manage.py migrate 
    ./manage.py collectstatic
    ```
6. Update the local Apache WSGI configuration to point to Django install & virtual environment. Relevant lines:

    (```/etc/apache/mods-enabled/wsgi.conf``` on Ubuntu)
    ```
    WSGIPythonPath /var/www/Roxy-Proxy/venv/lib/python2.7/site-packages:/var/www/Roxy-Proxy/roxy
    ```
    
    (```/etc/apache/sites-enabled/000-default``` on Ubuntu)
    ```
    WSGIScriptAlias / /var/www/Roxy-Proxy/roxy/roxy_master/wsgi.py
    Alias /static /var/www/Roxy-Proxy/roxy/static
    Alias /media /var/www/Roxy-Proxy/roxy/media
    ```
    
    Start Apache and login to ```http://my_hostname/admin/``` using the account set up on initial Django setup.
    
7. Update default Django site from pointing to example.com to point to server's hostname.
	
8. From the Django admin, add an ```Auth > Group``` object called ```Users```. Add ```User Profiles > Group Profile``` and set the proxy duration.
	
9. Setup Twisted proxy server. Set the proxy port number in  ```proxy/roxy.tac```:
    
    ```
    roxy_proxy = internet.TCPServer(8080, roxy_factory)
    ```

    Set the pointer to the Django instance in  ```roxy/roxy.py```:

    ```
    PROXY_MASTER = 'my_hostname'
    ```

10. Test proxy setup: ```twistd -ny roxy.tac``` If the server starts successfully, kill it with ```Ctrl-C``` and restart it in daemon mode: ```twistd -y roxy.tac```

11. In Django, add ```Proxy > Proxy Server``` object pointing to the Twisted proxy server. Make sure that the port and IP address is consistent with the Twisted settings above.

12. In the Django settings, add the host's IP address to ```roxy_master/settings.py```:

    ```
    INTERNAL_IPS = ('127.0.0.1', 'my_ip_address',)
    ```
    
    Restart Apache after making these changes.

13. Set up a local browser to use the Proxy server by following the instructions at ```http://my_hostname/setup```.

14. Test Django-Twisted connection by visiting ```http://my_host/proxy/proxy_test```.

    Note that if your server is on a private IP block (192.168.*, 10.*, etc.) or if your server has separate public and private IP addresses (Amazon EC2), this test will fail. Check the ```twisted.log``` file in theses cases to verify that the browser is using the Twistd proxy server. 

15. Verify that ```content/management/commands/fetch_content.py``` points to the right place to copy content to catalog. Check that the local paths match in  ```content/management/commands/catalog_content.py```, as well.

16. Set up Solr with Django Haystack 2.1.0:

    http://django-haystack.readthedocs.org/en/v2.1.0/
    
    A fixed ```schema.xml``` (for Solr 4.5 & 4.6) can be found in ```roxy/roxy_master/schema.xml```. Copy this file to ```solr/example/solr/collection1/conf/```. 
    
    When you're finished, in the ```solr/example``` folder, run ```nohup java start.jar &``` to initialize the Solr server. Log output will be sent to ```nohup.out```. 
	
17. Once Solr & Haystack are up and running, add ```roxy/update.sh``` to the local crontab. Verify that the paths referenced in that script match your configuration.

