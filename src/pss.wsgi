import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'pss.settings'
sys.path.append('/srv/django/participant-scheduling-system/src')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()