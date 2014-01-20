from BeautifulSoup import BeautifulSoup

import chardet
import json
import slate
import string
import sys
import traceback
import urlparse
import gzip

from django.core.urlresolvers import reverse
from django.db import models

import functions

class ContentRequest(models.Model):
    ip_address = models.IPAddressField(db_index=True)    
    
    url = models.URLField(max_length=2048, db_index=True)
    retrieved = models.DateTimeField(db_index=True)
    
    referrer_url = models.CharField(max_length=2048, null=True, blank=True, db_index=True)

    content_type = models.CharField(max_length=256, db_index=True)
    content_encoding = models.CharField(max_length=256, db_index=True)
    content_size = models.PositiveIntegerField(db_index=True)

    http_status = models.CharField(max_length=256, db_index=True)
    
    title = models.CharField(max_length=1024, null=True, blank=True, db_index=True)

    username = models.CharField(max_length=32, db_index=True)
    session_id = models.CharField(max_length=32, db_index=True)

    content_path = models.CharField(max_length=256, db_index=True)
    content_key = models.CharField(max_length=256, db_index=True)
    content_date = models.DateTimeField(db_index=True)
    
    def content_txt_url(self):
        return reverse('content_txt_url', args=(self.content_key,))

    def content_url(self):
        return reverse('content_url', args=(self.content_key,))
    
    def get_content(self):
        try:
            f = open(self.content_path, 'r')
        except IOError:
            f = open(string.replace(self.content_path, 'proxy_content', 'proxy_content/content'), 'r')
        
        content = None
        
        if self.content_encoding.strip().lower() == 'gzip':
            try:
                gf = gzip.GzipFile(fileobj=f, mode="rb")

                content = gf.read()            
            except:
                content = f.read()
        else:
            content = f.read()
            
        if string.find(self.content_type.lower(), 'utf-8') != -1:
            content = content.decode('utf-8')
        
        try:
            return content.encode("utf-8")
        except:
            pass
            
        return content
    
    def get_text_content(self):
        if self.content_type.lower().startswith('text/'):
            file_contents = self.get_content() # unicode(self.get_content(), errors='xmlcharrefreplace')
            
            result = chardet.detect(file_contents)
                
            if result['encoding'] != None:
                try:
                    return unicode(file_contents, result['encoding'])
                except:
                    return unicode('Error: ' + str(sys.exc_info()[1]))
            else:
                return 'NOT_A_TEXT_FILE'
        elif self.content_type.lower().startswith('application/pdf'):
            try:
                f = slate.PDF(open(self.content_path))
            
                file_contents = '' 

                for page in f:
                    file_contents += page

                result = chardet.detect(file_contents)
                    
                return unicode(file_contents, result['encoding'])
            except:
#                traceback.print_exc()
                pass

        return None
        
    def fetch_title(self):
        if self.title != None:
            return self.title

        try:
            if self.content_type.lower().startswith('text/html'):
                file_contents = self.get_content() # , errors='xmlcharrefreplace')
            
                html = BeautifulSoup(file_contents)
                data = html.find('title')
            
                if data != None and len(data) > 0:
                    title_str = data.contents[0]
                
                    self.title = title_str
                    self.save()
                    
                    return self.title
        except:
            pass
            
        return None
    

    def fetch_domains(self, omit_host=False):
        parsed = urlparse.urlparse(self.url)
        
        domains = []
        
        toks = string.split(str(parsed.hostname), '.')
        
        start_index = 0
        
        if omit_host:
            start_index = 1
        
        for i in range(start_index, len(toks) - 1):
            domains.append(string.join(toks[i:], '.'))
        
        return domains

    def fetch_referrer_domains(self):
        if self.referrer_url:
            parsed = urlparse.urlparse(self.referrer_url)
        
            domains = []
        
            try:
                toks = string.split(str(parsed.hostname), '.')
        
                for i in range(0, len(toks) - 1):
                    domains.append(string.join(toks[i:], '.'))
        
                return domains
            except:
                pass
        
        return []
        
    def fetch_search_terms(self):
        # TODO: Pull terms from referrer URL...
        return []

        
    def parent_score(self):
        sum = 0.0
        count = 0
        
        for estimator in ParentPageEstimator.objects.filter(enabled=True):
            score = estimator.evaluate(self)
            
            sum += (score * estimator.weight)
            count += estimator.weight
        
        score = 0.0
            
        if count > 0:
            score = sum / count
            
        return score


class ParentPageEstimator(models.Model):
    function_name = models.CharField(max_length=256, default='function_name')
    enabled = models.BooleanField(default=True)
    weight = models.PositiveIntegerField(default=1)
    
    def evaluate(self, content_request):
        return getattr(functions, self.function_name)(content_request)


class ContentReport(models.Model):
    report_type = models.CharField(max_length=256)

    period_start = models.DateTimeField()
    period_end = models.DateTimeField()

    report_contents = models.TextField(max_length=16384, default='{}')
    report_generated = models.DateTimeField()
    
    def fetch_contents(self):
        return json.loads(self.report_contents)
    
