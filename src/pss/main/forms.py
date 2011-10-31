from django import forms

from pss.main.models import Experiment, ExperimentDate, ExperimentDateTimeRange

class ExperimentForm(forms.ModelForm):
    # to-do: Be able to create qualifications and rooms.

    class Meta:
        model = Experiment

class ExperimentDateForm(forms.ModelForm):
    def __init__(self, experiment=None, *args, **kwargs):
        super(ExperimentDateForm, self).__init__(*args, **kwargs)
        self.experiment = experiment or self.instance.experiment

    def clean_date(self):
        date = self.cleaned_data['date']
        experiment_dates = ExperimentDate.objects.filter(experiment=self.experiment, date=date)
        if self.instance is not None:
            experiment_dates = experiment_dates.exclude(id=self.instance.id)
        if experiment_dates:
            raise forms.ValidationError('Experiment date with this Experiment and Date already exists.')
        return date

    class Meta:
        model = ExperimentDate
        exclude = ('experiment',)

class ExperimentDateTimeRangeForm(forms.ModelForm):
    class Meta:
        model = ExperimentDateTimeRange
        exclude = ('experiment_date',)