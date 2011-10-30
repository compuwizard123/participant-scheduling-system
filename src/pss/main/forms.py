from django import forms

from pss.main.models import Experiment, ExperimentDate, ExperimentDateTimeRange

# to-do: Enforce unique_together.

class ExperimentForm(forms.ModelForm):
    # to-do: Be able to create qualifications and rooms.

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