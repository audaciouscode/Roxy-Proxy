import string

from django.contrib.auth.models import Group
from django.db import models

from user_profiles.models import *

SESSION_TYPE = (
    ('active', 'Regular'),
    ('private', 'Private'),
    ('guest', 'Guest'),
)

class ContentTypeWhitelist(models.Model):
    regular_expression = models.CharField(max_length=128)
    enabled = models.BooleanField(default=True)

class Blacklist(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='blacklists')

    regular_expression = models.CharField(max_length=128)

    def display_string(self):
    	display_str = string.replace(self.regular_expression, '\\.', '.')
    	display_str = string.replace(display_str, '/', '')
    	
    	if display_str[0] == '.':
    		display_str = display_str[1:]
    		
    	return display_str

class GroupBlacklist(models.Model):
    group = models.ForeignKey(Group, related_name='blacklists')
    regular_expression = models.CharField(max_length=128)
    
class Session(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='sessions')

    ip_address = models.IPAddressField()    
    session_type = models.CharField(max_length=32, choices=SESSION_TYPE, default='active')

    session_start = models.DateTimeField()
    session_end = models.DateTimeField(blank=True, null=True)

    extension_duration = models.PositiveIntegerField(default=30)
    extensions = models.PositiveIntegerField(default=0)
    max_extensions = models.PositiveIntegerField(default=10)

class ProxyServer(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)
    
    ip_address = models.IPAddressField()    
    port = models.PositiveIntegerField(default=30)
    priority = models.PositiveIntegerField(default=30)

    def __unicode__(self):
        return self.name

class IpRedirect(models.Model):
    ip_address = models.IPAddressField()    
    url = models.CharField(max_length=4096, null=True, blank=True)
