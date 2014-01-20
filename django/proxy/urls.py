from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

from views import *

urlpatterns = patterns('',
    url(r'^session$', session, name='session'),
    url(r'^redirect$', redirect, name='redirect'),
    url(r'^history$', log_history, name='log_history'),
    url(r'^proxy_test$', proxy_test, name='proxy_test'),
    url(r'^temp_session/(?P<ip_address>.+)$', temp_session, name='temp_session'),
    url(r'^change_session$', change_session, name='change_session'),
    url(r'^(?P<server_slug>.+).pac$', pac_file, name='pac_file'),
)
