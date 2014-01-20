import datetime
import json
import logging

from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import Context, RequestContext, loader
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from user_profiles.models import *
from website.util import *

from models import *
from forms import *

@login_required
def proxy_test(request):
    context = RequestContext(request)
    context['ip_address'] = request.META['REMOTE_ADDR']
    
    using_roxy = False
    
    for server in ProxyServer.objects.all():
        if server.ip_address == context['ip_address']:
            using_roxy = True

    context['using_roxy'] = using_roxy
    
    return render_to_response(template_for_user('proxy_test.html', request.user), context)

def session(request):
    sessions = []
    
    if request.method == 'GET':
        ip_address = request.GET['ip_address']
        now = timezone.now()

        try:
            session = Session.objects.filter(ip_address=ip_address, session_start__lte=now, session_end__gte=now).order_by('-session_start')[0]
        except:
            return HttpResponse(json.dumps([]), mimetype="application/json")
    
        session_info = {}
        session_info['roxy_user'] = session.user_profile.user.username
        session_info['session_id'] = session.pk
        session_info['ip_address'] = ip_address
        session_info['type'] = session.session_type

        blacklist = []
        
        for group in session.user_profile.user.groups.all():
            for list_item in GroupBlacklist.objects.filter(group=group):
                blacklist.append(list_item.regular_expression)
                
                raw_domain = list_item.regular_expression[2:]

                blacklist.append('//' + raw_domain)
        
        for list_item in Blacklist.objects.filter(user_profile=session.user_profile):
            blacklist.append(list_item.regular_expression)

            raw_domain = list_item.regular_expression[2:]

            blacklist.append('//' + raw_domain)
            
        session_info['blacklist'] = blacklist
        
        content_whitelist = []
        
        for type_item in ContentTypeWhitelist.objects.filter(enabled=True):
            content_whitelist.append(type_item.regular_expression)
    
        session_info['content_types'] = content_whitelist

        sessions.append(session_info)

    return HttpResponse(json.dumps(sessions, sort_keys=True, indent=2), mimetype="application/json")

@csrf_exempt
def log_history(request):
    response_dict = {}

    profiles = {}
    
    if request.method == 'POST':
        json_payload = json.loads(request.POST['items'])
        
        for item in json_payload:
            session = None
            
            try:
                profiles[str(item['session_id'])]
            except:
                try:
                    session = Session.objects.get(pk=item['session_id'])
                    profiles[str(item['session_id'])] = session.user_profile
                except ObjectDoesNotExist:
                    pass
                except ValueError:
                    pass
                    
            try:
                hist_item = HistoryItem()
                hist_item.url = item['url'][:256]
                hist_item.mime_type = item['mime_type']
                hist_item.status_code = item['status_code']
                hist_item.content_key = item['content_key']

                hist_item.retrieved = datetime.datetime.fromtimestamp(item['retrieved'])
                hist_item.user_profile = profiles[str(item['session_id'])] 
            
                hist_item.save()
            except ObjectDoesNotExist:
                pass
            except KeyError:
                pass

        response_dict['status'] = 'ok'
    else:
        response_dict['status'] = 'error'
        response_dict['message'] = 'Invalid request.'

    return HttpResponse(json.dumps(response_dict), mimetype="application/json")

@login_required
def temp_session(request, ip_address):
    redirect_url = IpRedirect.objects.filter(ip_address=ip_address).order_by('-pk')[0]

    url = redirect_url.url

    if request.method == 'POST':
        form = SessionForm(request.POST)
        
        if form.is_valid():
            now = timezone.now()
            duration = datetime.timedelta(0, 0, 0, 0, request.user.profile.session_duration_setting())
            session_type = form.cleaned_data['session_type']

            session = Session(session_start=now, session_end=(now + duration), ip_address=ip_address, session_type=session_type)
            session.user_profile = request.user.profile
            
            session.save()

            return HttpResponseRedirect(url)
    else:
        form = SessionForm()

    context = RequestContext(request)
    context.update(csrf(request))
    context['form'] = form
    context['url'] = url
    context['ip_address'] = ip_address

    return render_to_response(template_for_user('new_session.html', request.user), context)

@login_required
def change_session(request):
    current_session_type = 'Unknown'

    if request.method == 'POST':
        form = SessionForm(request.POST)
        
        if form.is_valid():
            now = timezone.now()
            
            ip_address = request.META['REMOTE_ADDR']
            
            for session in request.user.profile.sessions.order_by('session_start'):
                if session.session_end == None or session.session_end >= now:
                    session.session_end = now
                    session.save()
                    
                    ip_address = session.ip_address
                    
                    if session.session_type == 'private':
                        current_session_type = 'Private'
                    elif session.session_type == 'regular':
                        current_session_type = 'Regular'
                    elif session.session_type == 'guest':
                        current_session_type = 'Guest'
           
            session_duration = request.user.profile.session_duration_setting()
            
            duration = datetime.timedelta(0, 0, 0, 0, session_duration)
            session_type = form.cleaned_data['session_type']

            session = Session(session_start=now, session_end=(now + duration), ip_address=ip_address, session_type=session_type)
            session.user_profile = request.user.profile
            
            session.save()

            return HttpResponseRedirect(reverse('user_home'))
    else:
        form = SessionForm()

    session = request.user.profile.sessions.order_by('-session_start')[0]
    
    if session.session_type == 'private':
        current_session_type = 'Private'
    elif session.session_type == 'active':
        current_session_type = 'Regular'
    elif session.session_type == 'guest':
        current_session_type = 'Guest'

    context = RequestContext(request)
    context.update(csrf(request))
    context['form'] = form
    context['current_session_type'] = current_session_type

    return render_to_response(template_for_user('change_session.html', request.user), context)


def redirect(request):
    url = request.GET['url']
    ip_address = request.GET['ip_address']
        
    redirect_url = IpRedirect(ip_address=ip_address, url=url)
    redirect_url.save()
    
    return HttpResponseRedirect(reverse('temp_session', args=[ip_address]))
    
    
def pac_file(request, server_slug):
    server = ProxyServer.objects.get(slug=server_slug)
    
    context = RequestContext(request)
    context['server'] = server
    return render_to_response('proxy.pac', context, mimetype='application/x-ns-proxy-autoconfig')
