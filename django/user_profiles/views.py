from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.template import loader, Context, RequestContext, TemplateDoesNotExist

from website.util import *

from models import *
from forms import *

@login_required
def edit_profile(request):
    context = RequestContext(request)

    updated = False    

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            
            request.user.save()
            
            profile = request.user.profile
            profile.session_duration = form.cleaned_data['session_duration']
            profile.save()
            
            updated = True
    else:
        initial = {}
        initial['email'] = request.user.email
        initial['first_name'] = request.user.first_name
        initial['last_name'] = request.user.last_name
        initial['session_duration'] = request.user.profile.session_duration_setting()
        
        form = ProfileForm(initial=initial)

    context = RequestContext(request)
    context['form'] = form
    context['updated'] = updated
    context.update(csrf(request))
    
    return render_to_response(template_for_user('user_profile.html', request.user), context)
