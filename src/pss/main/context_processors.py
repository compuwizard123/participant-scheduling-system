from datetime import date

from django.conf import settings

def pss_context_processor(request):
    year = date.today().year
    if year > 2011:
        year = u'2011-%s' % year
    return {
        'SITE_DOMAIN': settings.SITE_DOMAIN,
        'SITE_NAME': settings.SITE_NAME,
        'YEAR': year,
    }