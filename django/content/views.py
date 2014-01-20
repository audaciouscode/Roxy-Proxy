import csv
import chardet
import datetime
import html2text
import iso8601
import json

from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import get_current_site
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import loader, Context, RequestContext, TemplateDoesNotExist

from haystack.query import SearchQuerySet

from website.util import *

from models import *

@login_required
def solr_query(request):
    context = RequestContext(request)
    context.update(csrf(request))
    
    context['query'] = '*.*'
    
    if request.method == 'POST':
        results = SearchQuerySet().raw_search(request.POST['query'])

        context['results'] = results
        context['query'] = request.POST['query']

    return render_to_response(template_for_user('solr_query.html', request.user), context)

def solr_query_txt(request):
    results = SearchQuerySet().raw_search(request.GET['query'])
    
    output = 'id\tcontent_key\tip_address\tusername\turl\treferrer_url\thttp_status\tcontent_type\tcontent_size\tretrieved\tparent_score\tarchive_url\ttext_url\n'

    current_site = get_current_site(request)
    prefix = 'http://' + current_site.domain
    
    for result in results:
        if result.url != None:
            line = ''
        
            line += str(result.object.pk).strip() + '\t'
            line += result.object.content_key.strip() + '\t'
            line += result.object.ip_address.strip() + '\t'
            line += result.object.username.strip() + '\t'
            line += result.object.url.strip() + '\t'
        
            if result.referrer_url != None:
                line += result.object.referrer_url.strip() + '\t'
            else:
                line += '\t'
            
            line += result.object.http_status.strip() + '\t'
            line += result.object.content_type.strip() + '\t'
            line += str(result.object.content_size).strip() + '\t'
            line += str(result.object.retrieved).strip() + '\t'
            line += str(result.object.parent_score()).strip() + '\t'
            line += prefix + result.object.content_url().strip() + '\t'
            line += prefix + result.object.content_txt_url().strip() + '\n'
        
            output += line

    return HttpResponse(output, content_type="text/plain")

def content_url(request, key):
    obj = get_object_or_404(ContentRequest, content_key=key)
    return HttpResponse(obj.get_content(), content_type=obj.content_type.strip())

def content_txt_url(request, key):
    obj = get_object_or_404(ContentRequest, content_key=key)
    
    text = obj.get_text_content()

    return HttpResponse(html2text.html2text(text), content_type='text/plain')

def date_summary(request, start_date=None, end_date=None, report_type='date_report'):
    context = RequestContext(request)
    
    if start_date != None:
        date_toks = start_date.split('-')
        start_date = datetime.datetime(int(date_toks[0]), int(date_toks[1]), int(date_toks[2]), 0, 0, 0, 0)
    else:
        start_date = datetime.datetime(1900, 1, 1, 0, 0, 0, 0)

    if end_date != None:
        date_toks = end_date.split('-')
        end_date = datetime.datetime(int(date_toks[0]), int(date_toks[1]), int(date_toks[2]), 0, 0, 0, 0)
    else:
        end_date = datetime.datetime.now()

    context['start'] = start_date
    context['end'] = end_date
    
    try:
        report = ContentReport.objects.filter(report_type=report_type, period_start__gte=start_date, period_end__lte=end_date).order_by('-report_generated')[0]
    
        context['report'] = report
        context['report_contents'] = report.fetch_contents()
    except IndexError:
        pass
    
    return render_to_response(template_for_user('date_summary.html', request.user), context)

@login_required
def daily_summary(request, start_date=None, end_date=None, report_type='daily_report'):
    context = RequestContext(request)
    
    if start_date != None:
        date_toks = start_date.split('-')
        start_date = datetime.datetime(int(date_toks[0]), int(date_toks[1]), int(date_toks[2]), 0, 0, 0, 0)
    else:
        start_date = datetime.datetime(1900, 1, 1, 0, 0, 0, 0)

    if end_date != None:
        date_toks = end_date.split('-')
        end_date = datetime.datetime(int(date_toks[0]), int(date_toks[1]), int(date_toks[2]), 0, 0, 0, 0)
    else:
        end_date = datetime.datetime.now()

    context['start'] = start_date
    context['end'] = end_date
    
    try:
        report = ContentReport.objects.filter(report_type=report_type, period_start__gte=start_date, period_end__lte=end_date).order_by('-report_generated')[0]
    
        context['report'] = report
        context['report_contents'] = report.fetch_contents()
    except IndexError:
        pass
    
    return render_to_response(template_for_user('daily_report.html', request.user), context)

@login_required
def top_domains(request, start_date=None, end_date=None, report_type='top_domains_report'):
    context = RequestContext(request)
    
    if start_date != None:
        date_toks = start_date.split('-')
        start_date = datetime.datetime(int(date_toks[0]), int(date_toks[1]), int(date_toks[2]), 0, 0, 0, 0)
    else:
        start_date = datetime.datetime(1900, 1, 1, 0, 0, 0, 0)

    if end_date != None:
        date_toks = end_date.split('-')
        end_date = datetime.datetime(int(date_toks[0]), int(date_toks[1]), int(date_toks[2]), 0, 0, 0, 0)
    else:
        end_date = datetime.datetime.now()

    context['start'] = start_date
    context['end'] = end_date
    
    try:
        report = ContentReport.objects.filter(report_type=report_type, period_start__gte=start_date, period_end__lte=end_date).order_by('-report_generated')[0]
    
        context['report'] = report
        context['report_contents'] = report.fetch_contents()
    except IndexError:
        pass
    
    return render_to_response(template_for_user('top_ten_domains.html', request.user), context)

@login_required
def top_users(request, start_date=None, end_date=None, report_type='top_users_report'):
    context = RequestContext(request)
    
    if start_date != None:
        date_toks = start_date.split('-')
        start_date = datetime.datetime(int(date_toks[0]), int(date_toks[1]), int(date_toks[2]), 0, 0, 0, 0)
    else:
        start_date = datetime.datetime(1900, 1, 1, 0, 0, 0, 0)

    if end_date != None:
        date_toks = end_date.split('-')
        end_date = datetime.datetime(int(date_toks[0]), int(date_toks[1]), int(date_toks[2]), 0, 0, 0, 0)
    else:
        end_date = datetime.datetime.now()

    context['start'] = start_date
    context['end'] = end_date
    
    try:
        report = ContentReport.objects.filter(report_type=report_type, period_start__gte=start_date, period_end__lte=end_date).order_by('-report_generated')[0]
    
        context['report'] = report
        context['report_contents'] = report.fetch_contents()
    except IndexError:
        pass
    
    return render_to_response(template_for_user('top_ten_users.html', request.user), context)

@login_required
def top_types(request, start_date=None, end_date=None, report_type='top_types_report'):
    context = RequestContext(request)
    
    if start_date != None:
        date_toks = start_date.split('-')
        start_date = datetime.datetime(int(date_toks[0]), int(date_toks[1]), int(date_toks[2]), 0, 0, 0, 0)
    else:
        start_date = datetime.datetime(1900, 1, 1, 0, 0, 0, 0)

    if end_date != None:
        date_toks = end_date.split('-')
        end_date = datetime.datetime(int(date_toks[0]), int(date_toks[1]), int(date_toks[2]), 0, 0, 0, 0)
    else:
        end_date = datetime.datetime.now()

    context['start'] = start_date
    context['end'] = end_date
    
    try:
        report = ContentReport.objects.filter(report_type=report_type, period_start__gte=start_date, period_end__lte=end_date).order_by('-report_generated')[0]
    
        context['report'] = report
        context['report_contents'] = report.fetch_contents()
    except IndexError:
        pass
    
    return render_to_response(template_for_user('top_ten_types.html', request.user), context)
