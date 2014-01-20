# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ContentTypeWhitelist'
        db.create_table('proxy_contenttypewhitelist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('regular_expression', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('proxy', ['ContentTypeWhitelist'])

        # Adding model 'Blacklist'
        db.create_table('proxy_blacklist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_profile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='blacklists', to=orm['user_profiles.UserProfile'])),
            ('regular_expression', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('proxy', ['Blacklist'])

        # Adding model 'GroupBlacklist'
        db.create_table('proxy_groupblacklist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='blacklists', to=orm['auth.Group'])),
            ('regular_expression', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('proxy', ['GroupBlacklist'])

        # Adding model 'Session'
        db.create_table('proxy_session', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_profile', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sessions', to=orm['user_profiles.UserProfile'])),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('session_type', self.gf('django.db.models.fields.CharField')(default='active', max_length=32)),
            ('session_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('session_end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('extension_duration', self.gf('django.db.models.fields.PositiveIntegerField')(default=30)),
            ('extensions', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('max_extensions', self.gf('django.db.models.fields.PositiveIntegerField')(default=10)),
        ))
        db.send_create_signal('proxy', ['Session'])

        # Adding model 'ProxyServer'
        db.create_table('proxy_proxyserver', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=64)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('port', self.gf('django.db.models.fields.PositiveIntegerField')(default=30)),
            ('priority', self.gf('django.db.models.fields.PositiveIntegerField')(default=30)),
        ))
        db.send_create_signal('proxy', ['ProxyServer'])

        # Adding model 'IpRedirect'
        db.create_table('proxy_ipredirect', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=4096, null=True, blank=True)),
        ))
        db.send_create_signal('proxy', ['IpRedirect'])


    def backwards(self, orm):
        # Deleting model 'ContentTypeWhitelist'
        db.delete_table('proxy_contenttypewhitelist')

        # Deleting model 'Blacklist'
        db.delete_table('proxy_blacklist')

        # Deleting model 'GroupBlacklist'
        db.delete_table('proxy_groupblacklist')

        # Deleting model 'Session'
        db.delete_table('proxy_session')

        # Deleting model 'ProxyServer'
        db.delete_table('proxy_proxyserver')

        # Deleting model 'IpRedirect'
        db.delete_table('proxy_ipredirect')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'proxy.blacklist': {
            'Meta': {'object_name': 'Blacklist'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'regular_expression': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'blacklists'", 'to': "orm['user_profiles.UserProfile']"})
        },
        'proxy.contenttypewhitelist': {
            'Meta': {'object_name': 'ContentTypeWhitelist'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'regular_expression': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'proxy.groupblacklist': {
            'Meta': {'object_name': 'GroupBlacklist'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'blacklists'", 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'regular_expression': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'proxy.ipredirect': {
            'Meta': {'object_name': 'IpRedirect'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'null': 'True', 'blank': 'True'})
        },
        'proxy.proxyserver': {
            'Meta': {'object_name': 'ProxyServer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '30'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'default': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '64'})
        },
        'proxy.session': {
            'Meta': {'object_name': 'Session'},
            'extension_duration': ('django.db.models.fields.PositiveIntegerField', [], {'default': '30'}),
            'extensions': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'max_extensions': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10'}),
            'session_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'session_start': ('django.db.models.fields.DateTimeField', [], {}),
            'session_type': ('django.db.models.fields.CharField', [], {'default': "'active'", 'max_length': '32'}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessions'", 'to': "orm['user_profiles.UserProfile']"})
        },
        'user_profiles.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session_duration': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'setup_shown': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['proxy']