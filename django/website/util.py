import string
from urlparse import urlparse

from django.template import loader, Context, RequestContext, TemplateDoesNotExist

from user_profiles.models import *

def domain_to_expression(domain):
    return '\\.' + string.replace(domain, '.', '\\.') + '/'


def domains_for_user(user, limit=100):
    profile = user.profile
    
    query_limit = limit * 8
    
    domains = []
    hostnames = []
    
    need_more = True
    
    offset = 0
    
    while need_more:
        values_list = HistoryItem.objects.filter(user_profile=user.profile).order_by('-retrieved').values_list('url', 'retrieved', 'mime_type', 'status_code')[offset:(offset + query_limit)]

        for value in values_list:
            hostname = urlparse(value[0]).hostname
            
            if (hostname in hostnames) == False and len(domains) < limit:
                domain_dict = {}
                domain_dict['hostname'] = hostname
                domain_dict['last_retrieved'] = value[1]
                domain_dict['mime_type'] = value[2]
                domain_dict['status_code'] = value[3]
                
                domains.append(domain_dict)

                hostnames.append(hostname)
        
        if len(values_list) < limit:
            need_more = False
        elif len(domains) == limit:
            need_more = False

        offset += query_limit
        
    return domains

def template_for_user(template, user):
#    if user.is_authenticated():
#        lang = user.profile.language_setting()
#        
#        if lang == None:
#            lang = 'en'
#            
#        new_template = string.replace(template, '.html', '.' + lang + '.html')
#
#        try:
#            loader.get_template(new_template)
#            
#            return new_template
#        except TemplateDoesNotExist:
#            pass
        
    return template
