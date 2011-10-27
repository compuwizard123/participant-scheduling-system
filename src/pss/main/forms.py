from django import forms

from pss.main.models import Experiment, ExperimentDate, ExperimentDateTimeRange

class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment

class ExperimentDateForm(forms.ModelForm):
    class Meta:
        model = ExperimentDate
        exclude = ('experiment',)

class ExperimentDateTimeRangeForm(forms.ModelForm):
    class Meta:
        model = ExperimentDateTimeRange
        exclude = ('experiment_date',)