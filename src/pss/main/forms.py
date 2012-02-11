from datetime import datetime, timedelta

from django import forms
from django.contrib.auth.models import User
from django.db.models import Count

from pss.main.models import Experiment, ExperimentDate, ExperimentDateTimeRange, Participant, Researcher, Slot

class ExperimentForm(forms.ModelForm):
    def clean_number_of_participants_needed(self):
        number_of_participants_needed = self.cleaned_data['number_of_participants_needed']
        if self.instance.id is not None:
            m = max(Slot.objects.filter(experiment_date_time_range__experiment_date__experiment__id=self.instance.id) \
                    .annotate(appointment_count=Count('appointment')).values_list('appointment_count', flat=True))
            if number_of_participants_needed < m:
                raise forms.ValidationError('Ensure this value is greater than %s.' % max(0, m - 1))
        return number_of_participants_needed

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
    def __init__(self, experiment_date=None, *args, **kwargs):
        super(ExperimentDateTimeRangeForm, self).__init__(*args, **kwargs)
        self.experiment_date = experiment_date or self.instance.experiment_date

    def clean(self):
        cleaned_data = self.cleaned_data
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        if start_time is not None and end_time is not None:
            if start_time >= end_time:
                raise forms.ValidationError('The start time must be before the end time.')
            start_datetime = datetime.combine(self.experiment_date.date, start_time)
            end_datetime = datetime.combine(self.experiment_date.date, end_time)
            if (start_datetime + timedelta(minutes=self.experiment_date.experiment.length)).time() > end_datetime.time():
                raise forms.ValidationError('The start time and end time are too close.')
            experiment_date_time_ranges = ExperimentDateTimeRange.objects.filter(experiment_date=self.experiment_date,
                                                                                 start_time__lt=end_time,
                                                                                 end_time__gt=start_time)
            if self.instance is not None:
                experiment_date_time_ranges = experiment_date_time_ranges.exclude(id=self.instance.id)
            if experiment_date_time_ranges:
                raise forms.ValidationError('This experiment date time range conflicts with another one for this experiment date.')
            experiment_date_time_ranges = ExperimentDateTimeRange.objects.filter(experiment_date__experiment__room=self.experiment_date.experiment.room,
                                                                                 experiment_date__date=self.experiment_date.date,
                                                                                 start_time__lt=end_time,
                                                                                 end_time__gt=start_time)
            if self.instance is not None:
                experiment_date_time_ranges = experiment_date_time_ranges.exclude(id=self.instance.id)
            if experiment_date_time_ranges:
                raise forms.ValidationError('This experiment date time range conflicts with another one in this room.')
        return cleaned_data

    class Meta:
        model = ExperimentDateTimeRange
        exclude = ('experiment_date',)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        exclude = ('user',)

class ResearcherForm(forms.ModelForm):
    class Meta:
        model = Researcher
        exclude = ('user',)