from django.contrib import admin

from models import *

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'pac_url', 'date_joined', 'email',)
    list_filter = [ 'proxy_server', 'date_joined']

admin.site.register(UserProfile, UserProfileAdmin)

class GroupProfileAdmin(admin.ModelAdmin):
    list_display = ('group',)

admin.site.register(GroupProfile, GroupProfileAdmin)

class HistoryItemAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'hostname', 'retrieved', 'content_key', 'mime_type', 'status_code')
    list_filter = [ 'user_profile', 'retrieved', 'status_code']

admin.site.register(HistoryItem, HistoryItemAdmin)
