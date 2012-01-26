from django.conf.urls.defaults import *
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.shortcuts import get_object_or_404
from registration.forms import RegistrationForm

from pss.main import views
from pss.main.forms import ExperimentForm, ExperimentDateForm, ExperimentDateTimeRangeForm
from pss.main.models import Experiment, ExperimentDate, ExperimentDateTimeRange

def callback(request, *args, **kwargs):
    return {'user': request.user}

def validate_experiment_form_alt_callback(request, *args, **kwargs):
    return {'instance': get_object_or_404(Experiment, id=kwargs['id'], researchers__user=request.user)}

def validate_experiment_date_form_callback(request, *args, **kwargs):
    return {'experiment': get_object_or_404(Experiment, id=kwargs['id'], researchers__user=request.user)}

def validate_experiment_date_form_alt_callback(request, *args, **kwargs):
    return {'instance': get_object_or_404(ExperimentDate, id=kwargs['id'], experiment__researchers__user=request.user)}

def validate_experiment_date_time_range_form_callback(request, *args, **kwargs):
    return {'experiment_date': get_object_or_404(ExperimentDate, id=kwargs['id'], experiment__researchers__user=request.user)}

def validate_experiment_date_time_range_form_alt_callback(request, *args, **kwargs):
    return {'instance': get_object_or_404(ExperimentDateTimeRange, id=kwargs['id'], experiment_date__experiment__researchers__user=request.user)}

urlpatterns = patterns('',
    url(r'^$', views.index, name='main-index'),
    url(r'^experiments/$', views.experiments_view, name='main-list_experiments'),
    url(r'^experiments/create/$', views.experiment_view, name='main-create_experiment'),
    url(r'^experiments/edit/(?P<id>[\d]+)/$', views.experiment_view, name='main-edit_experiment'),
    url(r'^experiments/dates/(?P<experiment_id>[\d]+)/$', views.experiment_dates_view, name='main-list_experiment_dates'),
    url(r'^experiments/dates/create/(?P<experiment_id>[\d]+)/$', views.experiment_date_view, name='main-create_experiment_date'),
    url(r'^experiments/dates/edit/(?P<experiment_date_id>[\d]+)/$', views.experiment_date_view, name='main-edit_experiment_date'),
    url(r'^experiments/dates/time-ranges/(?P<experiment_date_id>[\d]+)/$', views.experiment_date_time_ranges_view, name='main-list_experiment_date_time_ranges'),
    url(r'^experiments/dates/time-ranges/create/(?P<experiment_date_id>[\d]+)/$', views.experiment_date_time_range_view, name='main-create_experiment_date_time_range'),
    url(r'^experiments/dates/time-ranges/edit/(?P<experiment_date_time_range_id>[\d]+)/$', views.experiment_date_time_range_view, name='main-edit_experiment_date_time_range'),
    url(r'^profile/$', views.profile, name='main-profile'),
    url(r'^appointments/$', views.appointments_view, name='main-list_appointments'),
    url(r'^appointments/sign-up/experiment/(?P<id>[\d]+)/$', views.sign_up_for_appointment_start, name='main-sign_up_for_appointment_start'),
    url(r'^appointments/sign-up/slot/(?P<id>[\d]+)/$', views.sign_up_for_appointment_finish, name='main-sign_up_for_appointment_finish'),
    url(r'^appointments/cancel/(?P<id>[\d]+)/$', views.cancel_appointment, name='main-cancel_appointment'),
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
    url(r'^ajax_validation/validate/experiment_form/$',
        'ajax_validation.views.validate',
        {'form_class': ExperimentForm},
        name='ajax_validation-validate_experiment_form'),
    url(r'^ajax_validation/validate/experiment_form_alt/(?P<id>[\d]+)/$',
        'ajax_validation.views.validate',
        {'form_class': ExperimentForm,
         'callback': validate_experiment_form_alt_callback},
        name='ajax_validation-validate_experiment_form_alt'),
    url(r'^ajax_validation/validate/experiment_date_form/(?P<id>[\d]+)/$',
        'ajax_validation.views.validate',
        {'form_class': ExperimentDateForm,
         'callback': validate_experiment_date_form_callback},
        name='ajax_validation-validate_experiment_date_form'),
    url(r'^ajax_validation/validate/experiment_date_form_alt/(?P<id>[\d]+)/$',
        'ajax_validation.views.validate',
        {'form_class': ExperimentDateForm,
         'callback': validate_experiment_date_form_alt_callback},
        name='ajax_validation-validate_experiment_date_form_alt'),
    url(r'^ajax_validation/validate/experiment_date_time_range_form/(?P<id>[\d]+)/$',
        'ajax_validation.views.validate',
        {'form_class': ExperimentDateTimeRangeForm,
         'callback': validate_experiment_date_time_range_form_callback},
        name='ajax_validation-validate_experiment_date_time_range_form'),
    url(r'^ajax_validation/validate/experiment_date_time_range_form_alt/(?P<id>[\d]+)/$',
        'ajax_validation.views.validate',
        {'form_class': ExperimentDateTimeRangeForm,
         'callback': validate_experiment_date_time_range_form_alt_callback},
        name='ajax_validation-validate_experiment_date_time_range_form_alt'),
)