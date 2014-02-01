import string

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import loader, Context, RequestContext, TemplateDoesNotExist

from proxy.models import Blacklist, Session
from user_profiles.models import *

from decorators import *
from forms import *
from util import *

def home(request):
    context = RequestContext(request)
    return render_to_response(template_for_user('home.html', request.user), context)

def about(request):
    context = RequestContext(request)
    return render_to_response(template_for_user('about.html', request.user), context)

def contact(request):
    form = ContactMessageForm()
    context = RequestContext(request)
    
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        
        if form.is_valid():
            sender = form.cleaned_data['sender']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            from_addr = sender + ' <' + email + '>'
            
            send_mail('Roxy Contact Form Message', message, from_addr, ['roxyhelpdesk@gmail.com'], fail_silently=False)

            return render_to_response(template_for_user('contact_done.html', request.user), context)

    context['form'] = form
    return render_to_response(template_for_user('contact.html', request.user), context)

@login_required
@show_setup
def user_home(request):
    context = RequestContext(request)
    
    context['domains'] = domains_for_user(request.user, 50)
    
    return render_to_response(template_for_user('user_home.html', request.user), context)

def page(request, page_name):
    context = RequestContext(request)

    return render_to_response(template_for_user('pages/' + page_name + '.html', request.user), context)

@login_required
def profile_redirect(request):
    return HttpResponseRedirect(reverse('user_home'))

@login_required
def history_txt(request):
    items = HistoryItem.objects.filter(user_profile=request.user.profile).order_by('retrieved')
    
    context = RequestContext(request)
    context['history_items'] = items

    return render_to_response('history.txt', context, mimetype='text/plain')

@login_required
@show_setup
def blacklist(request):
    form = BlacklistDomainForm()
    context = RequestContext(request)
    
    profile = request.user.get_profile()
    
    if request.method == 'POST':
        form = BlacklistDomainForm(request.POST)
        
        if form.is_valid():
            domain = form.cleaned_data['domain']
            
            blacklist_re = domain_to_expression(domain)
            
            if len(Blacklist.objects.filter(user_profile=profile, regular_expression=blacklist_re)) == 0:
                bl_obj = Blacklist(user_profile=profile, regular_expression=blacklist_re)
                bl_obj.save()
            
            context['domain'] = domain
            
            form = BlacklistDomainForm()

    context['form'] = form
    
    bl_domains = Blacklist.objects.filter(user_profile=profile).order_by('regular_expression')

    context['bl_domains'] = bl_domains
    
    context.update(csrf(request))
    
    return render_to_response(template_for_user('blacklist.html', request.user), context)

@login_required
@show_setup
def delete_blacklist(request, domain):
    blacklist_re = domain_to_expression(domain)
    profile = request.user.get_profile()
    
    to_remove = []
    
    for bl_obj in Blacklist.objects.filter(user_profile=profile, regular_expression=blacklist_re):
        to_remove.append(bl_obj)
        
    for bl_obj in to_remove:
        bl_obj.delete()

    return HttpResponseRedirect(reverse('blacklist'))
    
def about(request):
    context = RequestContext(request)
    return render_to_response(template_for_user('about.html', request.user), context)

def faq(request):
    context = RequestContext(request)
    return render_to_response(template_for_user('faq.html', request.user), context)

def setup(request):
    context = RequestContext(request)
    return render_to_response(template_for_user('setup.html', request.user), context)

def using(request):
    context = RequestContext(request)
    return render_to_response(template_for_user('using.html', request.user), context)
    
    
@login_required
@user_passes_test(lambda u: u.is_staff)
def last_login(request):
    all_sessions = Session.objects.order_by('-session_start')
    
    seen = []
    last_sessions = []
    
    for session in all_sessions:
        profile = session.user_profile
        if (profile in seen) == False:
            last_sessions.append(session)
            
            seen.append(profile)

    context = RequestContext(request)
    
    context['last_sessions'] = last_sessions
    
    return render_to_response('last_login.html', context)

