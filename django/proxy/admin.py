from django.contrib import admin

from models import *

class ContentTypeWhitelistAdmin(admin.ModelAdmin):
    list_display = ('regular_expression', 'enabled',)
    list_filter = ['enabled']

admin.site.register(ContentTypeWhitelist, ContentTypeWhitelistAdmin)


class GroupBlacklistAdmin(admin.ModelAdmin):
    list_display = ('group', 'regular_expression', )
    list_filter = ['group']

admin.site.register(GroupBlacklist, GroupBlacklistAdmin)


class BlacklistAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'regular_expression', )
    list_filter = ['user_profile']

admin.site.register(Blacklist, BlacklistAdmin)


class SessionAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'ip_address', 'session_type', 'session_start', 'session_end',)
    list_filter = [ 'session_type', 'session_start', 'session_end', 'user_profile',]

admin.site.register(Session, SessionAdmin)


class ProxyServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip_address', 'port',)

admin.site.register(ProxyServer, ProxyServerAdmin)


class IpRedirectAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'url',)

admin.site.register(IpRedirect, IpRedirectAdmin)
