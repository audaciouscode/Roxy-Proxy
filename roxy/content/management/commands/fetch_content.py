import subprocess

from django.core.management.base import BaseCommand, CommandError

from content.models import *

LOCAL_PATH = '/var/www/Roxy-Proxy/roxy/proxy_content/'
KEY_PATH = '/var/www/django/Roxy-Proxy/roxy_master/roxy_master/content/keys/id_rsa'
RSYNC_PATH = '/usr/bin/rsync'
SSH_PATH = '/usr/bin/ssh'

# rsync -av -e "ssh -i /home/thisuser/cron/thishost-rsync-key" remoteuser@remotehost:/remote/dir /this/dir/

class Command(BaseCommand):
    args = 'rsync path: remoteuser@remotehost:/remote/dir'
    help = 'Retrieves content from the proxy servers and catalogs it in Django.'

    def handle(self, *args, **options):
        command_line = [RSYNC_PATH]
        command_line.append('-av')
        
        if args[0].startswith('/') == False:
            command_line.append('-e')
            command_line.append(SSH_PATH + ' -i ' + KEY_PATH + ' -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no')

        command_line.append(args[0])
        command_line.append(LOCAL_PATH)
        
        print(str(command_line))
        
        subprocess.call(command_line, stdin=None, stdout=self.stdout, stderr=self.stderr)

