import datetime
import iso8601
import json
import operator
import os
import string
import subprocess

from optparse import make_option

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
            end = iso8601.parse_date(options['end'])
        
        self.stdout.write('Processing content collected between ' + start.strftime('%Y-%m-%d') + ' and ' + end.strftime('%Y-%m-%d') + '...\n')
        
        processed_count = 0
        
        date_counts = {}

        content_start = None
        content_end = None

        print('Building query...')
        
        query = ContentRequest.objects.filter(retrieved__gte=start, retrieved__lte=end)

        print('Calculating query length...')
        
        total = query.count()
        
        index = 0
        page_size = 1000
        
        while index < total:
            print('Fetching ' + str(index) + ' of ' + str(total) + '...')
            
            for request in query[index:(index+page_size)]:
                processed_count += 1
            
                date_key = request.retrieved.strftime('%Y-%m-%d')

                date_count = 0
                    
                try:
                    date_count = date_counts[date_key]
                except KeyError:
                    pass
                    
                date_counts[date_key] = date_count + 1
                    
                if content_start == None or content_start > request.retrieved:
                    content_start = request.retrieved

                if content_end == None or content_end < request.retrieved:
                    content_end = request.retrieved

            index += page_size

        sorted_dates = sorted(date_counts.iteritems(), key=operator.itemgetter(0), reverse=False)
        
        report = ContentReport(report_type='date_report')
        report.period_start = content_start
        report.period_end = content_end
        
        report.report_generated = datetime.datetime.now()
        
        contents_dict = {}
        
        parameters = {}
        parameters['start'] = start.isoformat()
        parameters['end'] = end.isoformat()

        contents_dict['parameters'] = parameters
        
        date_list = []
        
        for retrieval_date in sorted_dates:
            date_entry = {}
            
            date_entry['date'] = retrieval_date[0]
            date_entry['count'] = retrieval_date[1]

            date_list.append(date_entry)
        
        contents_dict['dates'] = date_list
        
        report.report_contents = json.dumps(contents_dict, indent=2)
        
        report.save()
        
        self.stdout.write('Processed ' + str(processed_count) + ' items...\n')
