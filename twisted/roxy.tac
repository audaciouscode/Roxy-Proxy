from twisted.application import service, internet

from twisted.web import resource, server, static
from twisted.web import proxy, http

import sys

sys.path.append(".")

from roxy import roxy

from twisted.internet import reactor
reactor.suggestThreadPoolSize(20)

application = service.Application("roxy")

# Proxy Server

roxy_factory = http.HTTPFactory()
roxy_factory.protocol = roxy.RoxyProxy

roxy_proxy = internet.TCPServer(8080, roxy_factory)
roxy_proxy.setServiceParent(application)

