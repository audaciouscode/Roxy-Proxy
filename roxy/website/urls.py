from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',
    url(r'^about$', about, name='about'),
    url(r'^faq$', faq, name='faq'),
    url(r'^setup$', setup, name='setup'),
    url(r'^using$', using, name='using'),
    url(r'^blacklist$', blacklist, name='blacklist'),
    url(r'^blacklist/delete/(?P<domain>.+)$', delete_blacklist, name='delete_blacklist'),
    url(r'^contact$', contact, name='contact'),
    url(r'^home$', user_home, name='user_home'),
    url(r'^export/history.txt$', history_txt, name='history_txt'),
    url(r'^pages/(?P<page_name>.+)$', page, name='page'),
    url(r'^accounts/profile', profile_redirect),
    url(r'^last_login$', last_login, name='last_login'),
    url(r'^$', home, name='home'),
)
