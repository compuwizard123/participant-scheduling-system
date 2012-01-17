from datetime import datetime, timedelta

from django import forms
from django.contrib.auth.models import User

from pss.main.models import Appointment, Experiment, ExperimentDate, ExperimentDateTimeRange, Participant, Researcher, Slot

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
    def __init__(self, experiment_date=None, *args, **kwargs):
        super(ExperimentDateTimeRangeForm, self).__init__(*args, **kwargs)
        self.experiment_date = experiment_date or self.instance.experiment_date

    # to-do: Include this logic in the admin too.
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

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ('participant',)

    def __init__(self, experiment, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['slot'].queryset = Slot.objects.filter(experiment_date_time_range__experiment_date__experiment=experiment)