from datetime import date

from django.conf import settings
from django.core.urlresolvers import reverse

def pss_context_processor(request):
    active = {
        'home': request.path == reverse('main-index'),
        'experiments': request.path.startswith(reverse('main-list_experiments')),
        'profile': request.path == reverse('main-profile') or request.path.startswith(reverse('auth_password_change')),
        'appointments': request.path.startswith(reverse('main-list_appointments')),
        'log_in': request.path == reverse('auth_login'),
        'sign_up': request.path.startswith(reverse('registration_register')),
    }
    year = date.today().year
    if year > 2011:
        year = u'2011-%s' % year
    return {
        'active': active,
        'SITE_DOMAIN': settings.SITE_DOMAIN,
        'SITE_NAME': settings.SITE_NAME,
        'YEAR': year,
    }