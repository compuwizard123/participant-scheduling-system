try:
    import json
except ImportError:
    import simplejson as json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import date, time

from pss.main.forms import ExperimentForm, ExperimentDateForm, ExperimentDateTimeRangeForm, UserForm, ParticipantForm, ResearcherForm
from pss.main.models import Appointment, Experiment, ExperimentDate, ExperimentDateTimeRange, Participant, Researcher, Slot

def index(request):
    return render_to_response('main/index.html',
                              RequestContext(request))

@login_required
def experiments_view(request):
    user = request.user
    try:
        researcher = user.researcher
    except Researcher.DoesNotExist:
        try:
            user.participant
        except Participant.DoesNotExist:
            # No profile
            messages.add_message(request, messages.ERROR, 'Please create a profile first.') # to-do: Better error
            return HttpResponseRedirect(reverse('main-profile'))
        # Participant
        is_researcher = False
        experiments = Experiment.objects.all()
    else:
        # Researcher
        is_researcher = True
        experiments = researcher.experiment_set.all()
    return render_to_response('main/experiments.html',
                              {'experiments': experiments,
                               'is_researcher': is_researcher},
                              RequestContext(request))

@login_required
def experiment_view(request, id=None):
    try:
        researcher = request.user.researcher
    except Researcher.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Permission denied') # to-do: Better error
        return HttpResponseRedirect(reverse('main-index'))
    if id is None:
        instance = None
        action = 'Create'
    else:
        instance = get_object_or_404(Experiment, id=id, researchers=researcher)
        action = 'Edit'
    if request.method == 'POST':
        if instance is not None and 'delete' in request.POST:
            instance.delete()
            messages.add_message(request, messages.SUCCESS, 'The experiment was successfully deleted.')
            return HttpResponseRedirect(reverse('main-list_experiments'))
        form = ExperimentForm(request.POST, instance=instance)
        if form.is_valid():
            db_instance = instance is not None and Experiment.objects.get(id=instance.id) or None
            experiment = form.save()
            experiment.researchers.add(researcher)
            experiment.save()
            if db_instance is not None and db_instance.length != experiment.length:
                Slot.objects.filter(experiment_date_time_range__experiment_date__experiment=experiment).delete()
                # to-do: Include warning.
                for experiment_date_time_range in ExperimentDateTimeRange.objects.filter(experiment_date__experiment=experiment):
                    experiment_date_time_range.create_slots()
            messages.add_message(request, messages.SUCCESS, 'The experiment was successfully saved.')
            return HttpResponseRedirect(reverse('main-list_experiments'))
    else:
        form = ExperimentForm(instance=instance)
    return render_to_response('main/experiment.html',
                              {'instance': instance,
                               'action': action,
                               'form': form},
                              RequestContext(request))

@login_required
def experiment_dates_view(request, experiment_id):
    try:
        researcher = request.user.researcher
    except Researcher.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Permission denied') # to-do: Better error
        return HttpResponseRedirect(reverse('main-index'))
    experiment = get_object_or_404(Experiment, id=experiment_id, researchers=researcher)
    return render_to_response('main/experiment_dates.html',
                              {'experiment': experiment},
                              RequestContext(request))

@login_required
def experiment_date_view(request, experiment_id=None, experiment_date_id=None):
    try:
        researcher = request.user.researcher
    except Researcher.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Permission denied') # to-do: Better error
        return HttpResponseRedirect(reverse('main-index'))
    if experiment_id is not None:
        instance = None
        action = 'Create'
        experiment = get_object_or_404(Experiment, id=experiment_id, researchers=researcher)
    else:
        instance = get_object_or_404(ExperimentDate, id=experiment_date_id, experiment__researchers=researcher)
        action = 'Edit'
        experiment = instance.experiment
    if request.method == 'POST':
        if instance is not None and 'delete' in request.POST:
            instance.delete()
            messages.add_message(request, messages.SUCCESS, 'The experiment date for %s was successfully deleted.' % experiment)
            return HttpResponseRedirect(reverse('main-list_experiment_dates', args=[experiment.id]))
        form = ExperimentDateForm(experiment, request.POST, instance=instance)
        if form.is_valid():
            experiment_date = form.save(commit=False)
            experiment_date.experiment = experiment
            experiment_date.save()
            messages.add_message(request, messages.SUCCESS, 'The experiment date for %s was successfully saved.' % experiment)
            return HttpResponseRedirect(reverse('main-list_experiment_dates', args=[experiment.id]))
    else:
        form = ExperimentDateForm(experiment, instance=instance)
    return render_to_response('main/experiment_date.html',
                              {'instance': instance,
                               'action': action,
                               'experiment': experiment,
                               'form': form},
                              RequestContext(request))

@login_required
def experiment_date_time_ranges_view(request, experiment_date_id):
    try:
        researcher = request.user.researcher
    except Researcher.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Permission denied') # to-do: Better error
        return HttpResponseRedirect(reverse('main-index'))
    experiment_date = get_object_or_404(ExperimentDate, id=experiment_date_id, experiment__researchers=researcher)
    return render_to_response('main/experiment_date_time_ranges.html',
                              {'experiment_date': experiment_date},
                              RequestContext(request))

@login_required
def experiment_date_time_range_view(request, experiment_date_id=None, experiment_date_time_range_id=None):
    try:
        researcher = request.user.researcher
    except Researcher.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Permission denied') # to-do: Better error
        return HttpResponseRedirect(reverse('main-index'))
    if experiment_date_id is not None:
        instance = None
        action = 'Create'
        experiment_date = get_object_or_404(ExperimentDate, id=experiment_date_id, experiment__researchers=researcher)
    else:
        instance = get_object_or_404(ExperimentDateTimeRange, id=experiment_date_time_range_id, experiment_date__experiment__researchers=researcher)
        action = 'Edit'
        experiment_date = instance.experiment_date
    if request.method == 'POST':
        if instance is not None and 'delete' in request.POST:
            instance.delete()
            messages.add_message(request, messages.SUCCESS, 'The experiment date time range for %s was successfully deleted.' % experiment_date)
            return HttpResponseRedirect(reverse('main-list_experiment_date_time_ranges', args=[experiment_date.id]))
        form = ExperimentDateTimeRangeForm(experiment_date, request.POST, instance=instance)
        if form.is_valid():
            db_instance = instance is not None and ExperimentDateTimeRange.objects.get(id=instance.id) or None
            experiment_date_time_range = form.save(commit=False)
            experiment_date_time_range.experiment_date = experiment_date
            experiment_date_time_range.save()
            _ = db_instance is not None and (db_instance.start_time != experiment_date_time_range.start_time or \
                                             db_instance.end_time != experiment_date_time_range.end_time)
            if _:
                experiment_date_time_range.slot_set.all().delete()
                # to-do: Include warning.
            if _ or instance is None:
                experiment_date_time_range.create_slots()
            messages.add_message(request, messages.SUCCESS, 'The experiment date time range for %s was successfully saved.' % experiment_date)
            return HttpResponseRedirect(reverse('main-list_experiment_date_time_ranges', args=[experiment_date.id]))
    else:
        form = ExperimentDateTimeRangeForm(experiment_date, instance=instance)
    return render_to_response('main/experiment_date_time_range.html',
                              {'instance': instance,
                               'action': action,
                               'experiment_date': experiment_date,
                               'form': form},
                              RequestContext(request))

@login_required
def profile(request):
    user_instance = request.user
    try:
        researcher_or_participant_instance = user_instance.researcher
        # editing researcher
    except Researcher.DoesNotExist:
        try:
            researcher_or_participant_instance = user_instance.participant
            # editing participant
        except Participant.DoesNotExist:
            researcher_or_participant_instance = None
            # creating participant
        ResearcherOrParticipantForm = ParticipantForm
    else:
        ResearcherOrParticipantForm = ResearcherForm
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user_instance)
        researcher_or_participant_form = ResearcherOrParticipantForm(request.POST, instance=researcher_or_participant_instance)
        if user_form.is_valid() and researcher_or_participant_form.is_valid():
            user = user_form.save()
            researcher_or_participant = researcher_or_participant_form.save(commit=False)
            researcher_or_participant.user = user
            researcher_or_participant.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Your profile was successfully saved.')
            return HttpResponseRedirect(reverse('main-profile'))
        messages.add_message(request, messages.ERROR,
                             'Please correct the errors below.')
    else:
        user_form = UserForm(instance=user_instance)
        researcher_or_participant_form = ResearcherOrParticipantForm(instance=researcher_or_participant_instance)
    return render_to_response('main/profile.html',
                              {'user_form': user_form,
                               'researcher_or_participant_form': researcher_or_participant_form},
                              RequestContext(request))

@login_required
def appointments_view(request):
    user = request.user
    try:
        participant = user.participant
    except Participant.DoesNotExist:
        try:
            user.researcher
        except Researcher.DoesNotExist:
            # No profile
            messages.add_message(request, messages.ERROR, 'Please create a profile first.') # to-do: Better error
            return HttpResponseRedirect(reverse('main-profile'))
        # Researcher
        messages.add_message(request, messages.ERROR, 'Please select an experiment.') # to-do: Better error
        return HttpResponseRedirect(reverse('main-list_experiments'))
    # Participant
    appointments = participant.appointment_set.all()
    return render_to_response('main/appointments.html',
                              {'appointments': appointments},
                              RequestContext(request))

@login_required
def participants_view(request, id):
    try:
        researcher = request.user.researcher
    except Researcher.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Permission denied') # to-do: Better error
        return HttpResponseRedirect(reverse('main-index'))
    experiment = get_object_or_404(Experiment, id=id, researchers=researcher)
    appointments = Appointment.objects.filter(slot__experiment_date_time_range__experiment_date__experiment=experiment)
    return render_to_response('main/participants.html',
                              {'experiment': experiment,
                               'appointments': appointments},
                              RequestContext(request))

def sign_up_for_appointment_start(request, id):
    """
    An AJAX view
    """
    if not request.is_ajax():
        messages.add_message(request, messages.ERROR, 'Permission denied') # to-do: Better error
        return HttpResponseRedirect(reverse('main-index'))
    if request.user.is_anonymous():
        return HttpResponse(json.dumps({'is_error': True, 'error': 'Anonymous user'})) # to-do: Better error
    try:
        participant = request.user.participant
    except Participant.DoesNotExist:
        return HttpResponse(json.dumps({'is_error': True, 'error': 'No profile'})) # to-do: Better error
    try:
        experiment = Experiment.objects.get(id=id)
    except Experiment.DoesNotExist:
        return HttpResponse(json.dumps({'is_error': True, 'error': 'Invalid ID'})) # to-do: Better error
    slots = []
    for slot in Slot.objects.filter(experiment_date_time_range__experiment_date__experiment=experiment):
        label = '%s: %s - %s' % (date(slot.experiment_date_time_range.experiment_date.date),
                                 time(slot.start_time),
                                 time(slot.end_time))
        url = reverse('main-sign_up_for_appointment_finish', args=[slot.id])
        is_disabled = False # to-do
        slots.append({'label': label, 'url': url, 'is_disabled': is_disabled})
    return HttpResponse(json.dumps({'is_error': False, 'slots': slots}))

def sign_up_for_appointment_finish(request, id):
    """
    An AJAX view
    """
    if not request.is_ajax():
        messages.add_message(request, messages.ERROR, 'Permission denied') # to-do: Better error
        return HttpResponseRedirect(reverse('main-index'))
    if request.user.is_anonymous():
        return HttpResponse('Anonymous user') # to-do: Better error
    try:
        participant = request.user.participant
    except Participant.DoesNotExist:
        return HttpResponse('No profile') # to-do: Better error
    try:
        slot = Slot.objects.get(id=id)
    except Slot.DoesNotExist:
        return HttpResponse('Invalid ID') # to-do: Better error
    # to-do: Validate slot.
    appointment, created = participant.appointment_set.get_or_create(slot=slot)
    if created:
        return HttpResponse('The appointment was successfully created.')
    else:
        return HttpResponse('The appointment is already created.')

def cancel_appointment(request, id):
    """
    An AJAX view
    """
    if not request.is_ajax():
        messages.add_message(request, messages.ERROR, 'Permission denied') # to-do: Better error
        return HttpResponseRedirect(reverse('main-index'))
    if request.user.is_anonymous():
        return HttpResponse('Anonymous user') # to-do: Better error
    try:
        participant = request.user.participant
    except Participant.DoesNotExist:
        return HttpResponse('No profile') # to-do: Better error
    try:
        appointment = participant.appointment_set.get(id=id)
    except Appointment.DoesNotExist:
        return HttpResponse('Invalid ID') # to-do: Better error
    if appointment.is_cancelled:
        return HttpResponse('The appointment is already cancelled.')
    appointment.is_cancelled = True
    appointment.save()
    return HttpResponse('The appointment was successfully cancelled.')