from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from pss.main.forms import ExperimentForm, ExperimentDateForm, ExperimentDateTimeRangeForm
from pss.main.models import Experiment, ExperimentDate, ExperimentDateTimeRange, Researcher

def index(request):
    return render_to_response('main/index.html',
                              RequestContext(request))

@login_required
def experiments_view(request):
    try:
        researcher = request.user.researcher
    except Researcher.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Permission denied') # to-do: Better error
        return HttpResponseRedirect(reverse('main-index'))
    experiments = researcher.experiment_set.all()
    return render_to_response('main/experiments.html',
                              {'experiments': experiments},
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
            experiment = form.save()
            experiment.researchers.add(researcher)
            experiment.save()
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
        form = ExperimentDateForm(request.POST, instance=instance)
        if form.is_valid():
            experiment_date = form.save(commit=False)
            experiment_date.experiment = experiment
            experiment_date.save()
            messages.add_message(request, messages.SUCCESS, 'The experiment date for %s was successfully saved.' % experiment)
            return HttpResponseRedirect(reverse('main-list_experiment_dates', args=[experiment.id]))
    else:
        form = ExperimentDateForm(instance=instance)
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
        form = ExperimentDateTimeRangeForm(request.POST, instance=instance)
        if form.is_valid():
            experiment_date_time_range = form.save(commit=False)
            experiment_date_time_range.experiment_date = experiment_date
            experiment_date_time_range.save()
            if instance is None:
                experiment_date_time_range.create_slots()
            else:
                pass # to-do
            messages.add_message(request, messages.SUCCESS, 'The experiment date time range for %s was successfully saved.' % experiment_date)
            return HttpResponseRedirect(reverse('main-list_experiment_date_time_ranges', args=[experiment_date.id]))
    else:
        form = ExperimentDateTimeRangeForm(instance=instance)
    return render_to_response('main/experiment_date_time_range.html',
                              {'instance': instance,
                               'action': action,
                               'experiment_date': experiment_date,
                               'form': form},
                              RequestContext(request))