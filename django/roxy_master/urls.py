from django.conf.urls import patterns, include, url

from haystack.query import SearchQuerySet
from haystack.views import SearchView

from content.forms import RoxyContentSearchForm

sqs = SearchQuerySet()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^accounts/', include('registration.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^proxy/', include('proxy.urls')),
    url(r'^profile/', include('user_profiles.urls')),
    url(r'^search/$', SearchView(
        searchqueryset=sqs,
        form_class=RoxyContentSearchForm
    ), name='haystack_search'),
    url(r'^content/', include('content.urls')),
    url(r'^', include('website.urls')),
)
