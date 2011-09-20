from django.conf.urls.defaults import *
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from registration.forms import RegistrationForm

from pss.main import views

def callback(request, *args, **kwargs):
    return {'user': request.user}

urlpatterns = patterns('',
    url(r'^$', views.index, name='main-index'),
    url(r'^ajax_validation/validate/authentication_form/$',
        'ajax_validation.views.validate',
        {'form_class': AuthenticationForm},
        name='ajax_validation-validate_authentication_form'),
    url(r'^ajax_validation/validate/password_change_form/$',
        'ajax_validation.views.validate',
        {'form_class': PasswordChangeForm, 'callback': callback},
        name='ajax_validation-validate_password_change_form'),
    url(r'^ajax_validation/validate/password_reset_form/$',
        'ajax_validation.views.validate',
        {'form_class': PasswordResetForm},
        name='ajax_validation-validate_password_reset_form'),
    url(r'^ajax_validation/validate/registration_form/$',
        'ajax_validation.views.validate',
        {'form_class': RegistrationForm},
        name='ajax_validation-validate_registration_form'),
    url(r'^ajax_validation/validate/set_password_form/$',
        'ajax_validation.views.validate',
        {'form_class': SetPasswordForm, 'callback': callback},
        name='ajax_validation-validate_set_password_form'),
)