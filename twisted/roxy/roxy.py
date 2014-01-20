import datetime
import httplib
import json
import os
import re
import smtplib
import sys
import time
import traceback
import urllib
import urlparse

from email.mime.text import MIMEText
from twisted.web import proxy, http

FOLDER = 'content/'
PROXY_MASTER = 'ec2-54-221-7-65.compute-1.amazonaws.com'
SESSIONS_URL = 'http://' + PROXY_MASTER + '/proxy/session'
REDIRECT_PATH = '/proxy/redirect?'
HISTORY_PATH = '/proxy/history'

HOST_WHITELIST = [PROXY_MASTER, 'fonts.googleapis.com', 'ajax.googleapis.com', 'platform.twitter.com']

HISTORY_QUEUE = []
HISTORY_QUEUE_LIMIT = 32
HISTORY_LAST_UPDATE = 0

def log_error(error_text):
    me = 'roxyproxy@audacious-software.com'
    you = 'roxyproxy@audacious-software.com'
    
    msg = MIMEText(error_text)
    
    msg['Subject'] = 'Roxy Proxy Error'
    msg['From'] = me 
    msg['To'] = you

    s = smtplib.SMTP('localhost')
    s.sendmail(me, [you], msg.as_string())
    s.quit()
    
def queue_history_item(hist_dict):
    global HISTORY_QUEUE
    global HISTORY_QUEUE_LIMIT
    global HISTORY_LAST_UPDATE
    
    HISTORY_QUEUE.append(hist_dict)

    now = time.time()
    
    expired = (now - HISTORY_LAST_UPDATE) > 60
    
    if expired or len(HISTORY_QUEUE) > HISTORY_QUEUE_LIMIT:
        hist_json = json.dumps(HISTORY_QUEUE)
        
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
        params = urllib.urlencode({ 'items': hist_json })

        conn = httplib.HTTPConnection(PROXY_MASTER)
        conn.request("POST", HISTORY_PATH, params, headers)

        response = conn.getresponse()
        
        try:
            response_dict = json.loads(response.read())
        except:
            log_error(traceback.format_exc())

        HISTORY_QUEUE = []
        HISTORY_LAST_UPDATE = now


class ContentWhitelist():
    def __init__(self, whitelist):
        self.expressions = []
        
        for item in whitelist:
            try:
                self.expressions.append(re.compile(item), re.IGNORECASE)
            except:
                log_error(traceback.format_exc())
        
    def allow(self, mime_type):
        for expression in self.expressions:
            if expression.search(mime_type) != None:
                return True
            
        return False


class Blacklist():
    def __init__(self, blacklist):
        self.expressions = []
        
        for item in blacklist:
            try:
                self.expressions.append(re.compile(item))
            except:
                log_error(traceback.format_exc())
        
    def allow(self, proxy_request):
        for expression in self.expressions:
            if expression.search(proxy_request.uri):
                return False
            
        return True


class SessionManager():
    def __init__(self):
        self.session_map = {}

    def session_for_request(self, proxy_request):
        ip_address = proxy_request.getClientIP()
        now = time.time()
        
        refresh_session = False
        
        if ip_address in self.session_map:
            refresh_session = ((now - self.session_map[ip_address]['last_update']) > 60)
        else:
            refresh_session = True
            
        if refresh_session:
            params = urllib.urlencode({ 'ip_address': ip_address })
            f = urllib.urlopen(SESSIONS_URL + '?%s' % params)
            json_string = f.read()
            
            sessions = json.loads(json_string)
            
            if len(sessions) == 0: # No session on server...
                return None

            new_session = sessions[0]
            new_session['last_update'] = now

            new_session['blacklist'] = Blacklist(new_session['blacklist'])
            new_session['roxy_user'] = new_session['roxy_user']
            new_session['content_types'] = ContentWhitelist(new_session['content_types'])
            
            self.session_map[ip_address] = new_session
        
        return self.session_map[ip_address]

    def session_id(self, proxy_request):
        session = self.session_for_request(proxy_request)
        return session['session_id']

    def session_user(self, proxy_request):
        session = self.session_for_request(proxy_request)
        return session['roxy_user']
            
    def is_active(self, proxy_request):
        session = self.session_for_request(proxy_request)

        if session == None:
            return False
            
        return True

    def log_request(self, proxy_request):
        session = self.session_for_request(proxy_request)

        if session['type'] == 'guest':
            return False
            
    def log_content_type(self, client):
        session = self.session_for_request(client.father)

        if client.history_mime != '':
            return session['content_types'].allow(client.history_mime)

        return False

SESSIONS = SessionManager()

class RoxyProxyClient(proxy.ProxyClient):
    def __init__(self, command, rest, version, headers, data, father):
        proxy.ProxyClient.__init__(self, command, rest, version, headers, data, father)
        
        self.fetched = datetime.datetime.now()
        self.timestamp = time.time()
        self.log_request = True

        self.metadata = self.open_file('metadata')
        self.content = self.open_file('content')
        
        self.history_key = ('%f' % self.timestamp)
        self.history_retrieved = self.timestamp
        self.history_session_id = ''
        self.history_url = ''
        self.history_mime = ''
        self.history_status_code = ''
        
        self.client_headers = headers
        
        
    def open_file(self, name):
        ip_address = self.father.getClientIP()
        
        folder = FOLDER + 'ip_' + ip_address + '/' + self.fetched.strftime('%Y/%m/%d/%H/%M')
        
        if not os.path.exists(folder): 
            os.makedirs(folder)
        
        filename = folder + '/' + ('%f' % self.timestamp) + '-' + name
        
        f = open(filename, 'ab')
        
        return f
        
    def connectionMade(self):
        if self.log_request:
            self.metadata.write(self.father.method + ' ' + str(self.father.uri) + '\n')
            self.metadata.write(self.father.method + ' Arguments: ' + json.dumps(self.father.args) + '\n')

            self.history_url = str(self.father.uri) 
            
            if self.client_headers != None:
                for key, value in self.client_headers.iteritems():
                    key = "client:" + key

                    self.metadata.write(key + ': ' + value + '\n')

        proxy.ProxyClient.connectionMade(self)

    def handleHeader(self, key, value):
        if self.log_request:
            self.metadata.write(key + ': ' + value + '\n')

            if key.lower() == 'content-type':
                self.history_mime = value
                
                if SESSIONS.log_content_type(self) == False:
                    self.metadata.write('X-Roxy-Content-Logged: false\n')
                else:
                    self.metadata.write('X-Roxy-Content-Logged: true\n')
        
        proxy.ProxyClient.handleHeader(self, key, value)

    def handleResponsePart(self, buffer): 
        if self.log_request and SESSIONS.log_content_type(self):
            self.content.write(buffer)

        proxy.ProxyClient.handleResponsePart(self, buffer)
    
    def handleStatus(self, version, code, message):
        if self.log_request:
            self.metadata.write(version + ' ' + str(code) + ' ' + message + '\n')
            self.handleHeader('X-Roxy-Session-ID', str(SESSIONS.session_id(self.father)))
            self.handleHeader('X-Roxy-User', str(SESSIONS.session_user(self.father)))

            self.history_status_code = str(code) + ' ' + message
            self.history_session_id = SESSIONS.session_id(self.father)

        proxy.ProxyClient.handleStatus(self, version, code, message)

    def handleResponseEnd(self):
        self.metadata.close()
        self.content.close()

        hist_item = {}
        hist_item['content_key'] = self.history_key
        hist_item['retrieved'] = self.history_retrieved
        hist_item['session_id'] = self.history_session_id
        hist_item['url'] = self.history_url[:128]
        hist_item['mime_type'] = self.history_mime
        hist_item['status_code'] = self.history_status_code

        queue_history_item(hist_item)
        
        proxy.ProxyClient.handleResponseEnd(self)
                

class RoxyProxyClientFactory(proxy.ProxyClientFactory):
    protocol = RoxyProxyClient


class RoxyProxyRequest(proxy.ProxyRequest):
    protocols = {'http': RoxyProxyClientFactory}
    ports = {'http': 80}
        
    def process(self):
        parsed = urlparse.urlparse(self.uri)
        
        host = parsed[1]
        port = 80
        headers = self.getAllHeaders().copy()
            
        if ':' in host:
            host, port = host.split(':')
            port = int(port)

        rest = urlparse.urlunparse(('', '') + parsed[2:])

        if SESSIONS.is_active(self) and (host in HOST_WHITELIST) == False:
            if not rest:
                rest = rest + '/'

            headers["X-Forwarded-For"] = self.getClientIP()

            self.content.seek(0, 0)
            s = self.content.read()
            clientFactory = RoxyProxyClientFactory(self.method, rest, self.clientproto, headers, s, self)
            
            if SESSIONS.log_request(self) == False:
                clientFactory = proxy.ProxyClientFactory(self.method, rest, self.clientproto, headers, s, self)
            
            self.reactor.connectTCP(host, port, clientFactory)
        else:
            headers['host'] = PROXY_MASTER

            self.content.seek(0, 0)
            s = self.content.read()
            
            args = (('url', self.uri), ('ip_address', self.getClientIP()),)
            
            clientFactory = proxy.ProxyClientFactory(self.method, REDIRECT_PATH + urllib.urlencode(args), self.clientproto, headers, s, self)
            
            if host in HOST_WHITELIST:
                headers['host'] = host
                clientFactory = proxy.ProxyClientFactory(self.method, rest, self.clientproto, headers, s, self)
                self.reactor.connectTCP(host, 80, clientFactory)
            else:
                self.reactor.connectTCP(PROXY_MASTER, 80, clientFactory)
        

class RoxyProxy(proxy.Proxy):
    requestFactory = RoxyProxyRequest
