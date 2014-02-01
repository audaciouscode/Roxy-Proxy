from urlparse import urlparse

from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import gettext_noop

LANGUAGES = (
    ('en', gettext_noop('English')),
    ('es', gettext_noop('Spanish')),
    ('he', gettext_noop('Hebrew')),
)

DEFAULT_GROUP_NAME = 'Users'

def get_default_group():
    return Group.objects.get(name=DEFAULT_GROUP_NAME)

def get_default_proxy():
    from proxy.models import ProxyServer

    return ProxyServer.objects.order_by('-priority')[0]

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    proxy_server = models.ForeignKey('proxy.ProxyServer', null=True, blank=True, default=get_default_proxy)
    session_duration = models.SmallIntegerField(null=True, blank=True)
    setup_shown = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(null=True, blank=True)
    
    def __unicode__(self):
        return self.user.username

    def email(self):
        return self.user.email
    
    def pac_url(self):
        do_save = False
        
        if self.date_joined == None:
            self.date_joined = self.user.date_joined
            
            self.save()
            
        return 'http://' + Site.objects.all()[0].domain + reverse('pac_file', args=[self.proxy_server.slug])

    def session_duration_setting(self):
        if self.session_duration != None:
            return self.session_duration

        group_profile = self.group_profile()
        
        if group_profile:
            return group_profile.session_duration
        
        return 60
            
    def group_profile(self):
        groups = self.user.groups.all()    
        
        if len(groups) == 0:
            default_group = get_default_group()
            
            default_group.user_set.add(self.user)
            default_group.save()
            
            return self.group_profile()
        
        for group in groups:
            for group_profile in GroupProfile.objects.filter(group=group):
                return group_profile
            
        return None
        
#    def last_login(self):
#        return self.user.last_login
        
#    def date_joined(self):
#        return self.user.date_joined

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class GroupProfile(models.Model):
    group = models.ForeignKey(Group, related_name='profiles')
    session_duration = models.SmallIntegerField(default=60)
    
    def __unicode__(self):
        return self.group.name


class HistoryItem(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    
    url = models.CharField(max_length=256)
    retrieved = models.DateTimeField()
    mime_type = models.CharField(max_length=128)

    content_key = models.CharField(max_length=256)
    status_code = models.CharField(max_length=256)
        
    def __unicode__(self):
        return self.url

    def hostname(self):
        return urlparse(self.url).hostname
