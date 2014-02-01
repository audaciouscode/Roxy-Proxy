from django.contrib import admin

from models import *

class ContentRequestAdmin(admin.ModelAdmin):
    list_display = ('username', 'title', 'retrieved', 'http_status', 'content_type', 'content_size',)
    list_filter = [ 'username', 'retrieved', 'http_status', 'content_type' ]

admin.site.register(ContentRequest, ContentRequestAdmin)

class ParentPageEstimatorAdmin(admin.ModelAdmin):
    list_display = ('function_name', 'weight', 'enabled',)

admin.site.register(ParentPageEstimator, ParentPageEstimatorAdmin)

class ContentReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'period_start', 'period_end', 'report_generated',)
    list_filter = [ 'report_type', 'period_start', 'period_end', 'report_generated' ]

admin.site.register(ContentReport, ContentReportAdmin)
