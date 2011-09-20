from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def mungify(email):
    if '@' not in email:
        email += '@' + settings.SITE_DOMAIN
    return mark_safe(''.join(['&#%s;' % (ord(c)) for c in email]))