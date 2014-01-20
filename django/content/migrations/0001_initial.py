# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ContentRequest'
        db.create_table('content_contentrequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15, db_index=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=2048, db_index=True)),
            ('retrieved', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('referrer_url', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=2048, null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.CharField')(max_length=256, db_index=True)),
            ('content_encoding', self.gf('django.db.models.fields.CharField')(max_length=256, db_index=True)),
            ('content_size', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('http_status', self.gf('django.db.models.fields.CharField')(max_length=256, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=1024, null=True, blank=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('session_id', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('content_path', self.gf('django.db.models.fields.CharField')(max_length=256, db_index=True)),
            ('content_key', self.gf('django.db.models.fields.CharField')(max_length=256, db_index=True)),
            ('content_date', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
        ))
        db.send_create_signal('content', ['ContentRequest'])

        # Adding model 'ParentPageEstimator'
        db.create_table('content_parentpageestimator', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('function_name', self.gf('django.db.models.fields.CharField')(default='function_name', max_length=256)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('weight', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal('content', ['ParentPageEstimator'])

        # Adding model 'ContentReport'
        db.create_table('content_contentreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report_type', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('period_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('period_end', self.gf('django.db.models.fields.DateTimeField')()),
            ('report_contents', self.gf('django.db.models.fields.TextField')(default='{}', max_length=16384)),
            ('report_generated', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('content', ['ContentReport'])


    def backwards(self, orm):
        # Deleting model 'ContentRequest'
        db.delete_table('content_contentrequest')

        # Deleting model 'ParentPageEstimator'
        db.delete_table('content_parentpageestimator')

        # Deleting model 'ContentReport'
        db.delete_table('content_contentreport')


    models = {
        'content.contentreport': {
            'Meta': {'object_name': 'ContentReport'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period_end': ('django.db.models.fields.DateTimeField', [], {}),
            'period_start': ('django.db.models.fields.DateTimeField', [], {}),
            'report_contents': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'max_length': '16384'}),
            'report_generated': ('django.db.models.fields.DateTimeField', [], {}),
            'report_type': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'content.contentrequest': {
            'Meta': {'object_name': 'ContentRequest'},
            'content_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'content_encoding': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'content_key': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'content_path': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'content_size': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'http_status': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'db_index': 'True'}),
            'referrer_url': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'retrieved': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'session_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '2048', 'db_index': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'})
        },
        'content.parentpageestimator': {
            'Meta': {'object_name': 'ParentPageEstimator'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'function_name': ('django.db.models.fields.CharField', [], {'default': "'function_name'", 'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'weight': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['content']