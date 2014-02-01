import datetime
import iso8601
import json
import operator
import os
import string
import subprocess
import tempfile

from optparse import make_option

from django.core.mail import *
from django.core.management.base import BaseCommand, CommandError

from content.models import *
        
class Command(BaseCommand):
    help = 'Generates report objects from the content showing the top users for a given time period.'

    option_list = BaseCommand.option_list + (
        make_option('--start',
            dest='start',
            default=None,
            help='Period to start generating reports. Format using ISO 8601 UTC (2012-08-14T19:39Z).'),
        make_option('--end',
            dest='end',
            default=None,
            help='Period to stop generating reports. Format using ISO 8601 UTC.'),
        )

    def handle(self, *args, **options):
        start = datetime.datetime(1900, 1, 1, 0, 0, 0, 0)
        end = datetime.datetime.now()

        if options['start']:
            start = iso8601.parse_date(options['start'])

        if options['end']:
            start = iso8601.parse_date(options['end'])
        
        self.stdout.write('Processing content collected between ' + start.strftime('%Y-%m-%d') + ' and ' + end.strftime('%Y-%m-%d') + '...\n')

        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        
        tmp_file.write('username\tip_address\turl\tretrieved\treferrer\tcontent_type\tcontent_encoding\tsize\thttp_status\ttitle\tsession\tpath\tkey\timported\n')
        
        for request in ContentRequest.objects.filter(retrieved__gte=start, retrieved__lte=end).order_by('retrieved'):
            line = request.username.strip() + '\t'
            line += request.ip_address.strip() + '\t'
            line += request.url.strip() + '\t'
            line += request.retrieved.isoformat().strip() + '\t'

            if request.referrer_url != None:
                line += request.referrer_url.strip() + '\t'
            else:
                line += '\t'

            line += request.content_type.strip() + '\t'
            line += request.content_encoding.strip() + '\t'
            line += str(request.content_size).strip() + '\t'
            line += request.http_status.strip() + '\t'

            if request.title != None:
                line += request.title.strip() + '\t'
            else:
                line += '\t'

            line += str(request.session_id).strip() + '\t'
            line += request.content_path.strip() + '\t'
            line += request.content_key.strip() + '\t'
            line += request.content_date.isoformat().strip() + '\n'
            
            tmp_file.write(line.encode('ascii', 'xmlcharrefreplace'))

        tmp_file.flush()
        tmp_file.close()
        
        print('FILE: ' + tmp_file.name)
