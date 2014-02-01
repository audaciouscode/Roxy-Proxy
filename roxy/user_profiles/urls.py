from django.conf.urls.defaults import *
# from django.views.generic.simple import redirect_to

from views import *

urlpatterns = patterns('',
     url(r'^edit$', edit_profile, name='edit_profile'),
)
