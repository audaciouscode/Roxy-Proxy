import datetime
import icu
import os
import string
import subprocess
import traceback

from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction

from content.models import *

LOCAL_PATH = '/var/www/Roxy-Proxy/roxy/proxy_content/'

def convert_encoding(data, new_coding='UTF-8'):
    coding = icu.CharsetDetector(data).detect().getName()
    if new_coding.upper() != coding.upper():
        data = unicode(data, coding).encode(new_coding)
    return data

def is_cataloged(path, path_map):
    path = string.replace(path, '-metadata', '-content')
    
    try:
        return path_map[path]
    except KeyError:
        pass
    
    return False

def stored_paths():
    path_map = {}

    for path in  ContentRequest.objects.values_list('content_path', flat=True).distinct():
        path_map[path] = True
        
    return path_map

def catalog(path, stdout):

    file_path = string.replace(path, '-metadata', '-content')
    
    if ContentRequest.objects.filter(content_path=file_path).count() == 0:
        transaction.commit_unless_managed()
   
        stdout.write('Cataloging ' + path + '...')
    
        request = ContentRequest()
    
        request.retrieved  = datetime.datetime.utcfromtimestamp(0)
        request.content_path = file_path
        request.content_size = os.path.getsize(file_path)

        content_time = os.stat(file_path).st_ctime

        request.content_date = datetime.datetime.utcfromtimestamp(content_time)

    for tok in string.split(path, '/'):
        if tok.startswith('ip_'):
            request.ip_address = string.replace(tok, 'ip_', '')
        elif tok.endswith('-metadata'):
            request.content_key = string.replace(tok, '-metadata', '')
            request.retrieved = datetime.datetime.utcfromtimestamp(float(request.content_key))
    
    f = open(path, 'r')
    
    try:
        for line in f:
            if line.startswith('GET http://'):
                request.url = convert_encoding(string.replace(line, 'GET ', '')[:2048])
            elif line.startswith('HTTP/'):
                request.http_status = convert_encoding(line[:256])
            elif line.startswith('X-Roxy-User: '):
                request.username = convert_encoding(string.replace(line, 'X-Roxy-User: ', ''))
            elif line.startswith('X-Roxy-Session-ID: '):
                request.session_id = convert_encoding(string.replace(line, 'X-Roxy-Session-ID: ', ''))
            elif line.startswith('Content-Encoding: '):
                request.content_encoding = convert_encoding(string.replace(line, 'Content-Encoding: ', ''))
            elif line.startswith('Content-Type: '):
                request.content_type = convert_encoding(string.replace(line, 'Content-Type: ', ''))
            elif line.startswith('client:referer: '):
                request.referrer_url = convert_encoding(string.replace(line, 'client:referer: ', ''))
    
        try:
            request.save()
        except:
            traceback.print_exc()
            connection._rollback()
    except:
        traceback.print_exc()
        
    stdout.write(' done.\n')
        
class Command(BaseCommand):
    args = 'None'
    help = 'Catalogs content retrieved from proxy servers.'

    def handle(self, *args, **options):
        files = []

        path_map = stored_paths()
        
        paths = list(os.walk(LOCAL_PATH))
        
        path_count = len(paths)
        print('paths count ' + str(path_count))
        path_index = 0

        to_catalog = []
        
        for root, dir, files in paths:
            file_count = len(files)

            file_index = 0
            
            for file in files:
                path = root + '/' + file
                
                if path.endswith('-metadata') and is_cataloged(path, path_map) == False:
                    to_catalog.append(path)
                    
                file_index += 1

            path_index += 1
        
        counter = 0
        
        for path in to_catalog:
            catalog(path, self.stdout)
            counter += 1
            print('Progress: ' + str(counter) + '/' + str(len(to_catalog)))

