# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ContactMessage'
        db.create_table('website_contactmessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.CharField')(max_length=51)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=512)),
            ('message', self.gf('django.db.models.fields.TextField')(max_length=4096)),
            ('sent', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('website', ['ContactMessage'])


    def backwards(self, orm):
        # Deleting model 'ContactMessage'
        db.delete_table('website_contactmessage')


    models = {
        'website.contactmessage': {
            'Meta': {'object_name': 'ContactMessage'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'max_length': '4096'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '51'}),
            'sent': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['website']