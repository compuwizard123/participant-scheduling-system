from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from pss.main.forms import ExperimentForm, ExperimentDateForm, ExperimentDateTimeRangeForm
from pss.main.models import Experiment, Researcher

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
                              {'action': action,
                               'form': form},
                              RequestContext(request))