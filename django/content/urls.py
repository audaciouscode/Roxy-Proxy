from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',
    url(r'^reports/date_summary/(?P<start_date>[0-9\-]+)$', date_summary, name='date_summary_start_only'),
    url(r'^reports/daily_summary/(?P<start_date>[0-9\-]+)$', daily_summary, name='daily_summary_start_only'),

    url(r'^reports/top_domains/(?P<start_date>[0-9\-]+)$', top_domains, name='top_domains_start_only'),
    url(r'^reports/top_domains/(?P<start_date>[0-9\-]+)/(?P<end_date>[0-9\-]+)$', top_domains, name='top_domains'),

    url(r'^reports/top_users/(?P<start_date>[0-9\-]+)$', top_users, name='top_users_start_only'),
    url(r'^reports/top_users/(?P<start_date>[0-9\-]+)/(?P<end_date>[0-9\-]+)$', top_users, name='top_users'),

    url(r'^reports/top_types/(?P<start_date>[0-9\-]+)$', top_types, name='top_typesstart_only'),
    url(r'^reports/top_types/(?P<start_date>[0-9\-]+)/(?P<end_date>[0-9\-]+)$', top_types, name='top_types'),

    url(r'^content/text/(?P<key>.+)$', content_txt_url, name='content_txt_url'),
    url(r'^content/original/(?P<key>.+)$', content_url, name='content_url'),
    url(r'^content/solr$', solr_query, name='solr_query'),
    url(r'^content/txt/solr$', solr_query_txt, name='solr_query_txt'),
)
