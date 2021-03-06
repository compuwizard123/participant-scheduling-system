from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField
from django.core.exceptions import ValidationError
from django.db import models

class Participant(models.Model):
    user = models.OneToOneField(User, unique=True,
                                limit_choices_to={'researcher__isnull': True})
    # Already stores name and email:
    #   user.first_name
    #   user.last_name
    #   user.email
    phone_number = PhoneNumberField()

    class Meta:
        ordering = ('user__last_name', 'user__first_name', 'user__username',)

    def __unicode__(self):
        return self.user.get_full_name() or self.user.username

class Researcher(models.Model):
    user = models.OneToOneField(User, unique=True,
                                limit_choices_to={'participant__isnull': True})
    # Already stores name and email:
    #   user.first_name
    #   user.last_name
    #   user.email
    phone_number = PhoneNumberField()

    class Meta:
        ordering = ('user__last_name', 'user__first_name', 'user__username',)

    def __unicode__(self):
        return self.user.get_full_name() or self.user.username

class Building(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

class Room(models.Model):
    building = models.ForeignKey(Building)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('building', 'name',)
        unique_together = (('building', 'name',),)

    def __unicode__(self):
        return '%s %s' % (self.building, self.name)

class Qualification(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

class NonZeroPositiveSmallIntegerField(models.SmallIntegerField):
    def validate(self, value, model_instance):
        if value <= 0:
            raise ValidationError('Ensure this value is greater than 0.')

class Experiment(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    researchers = models.ManyToManyField(Researcher)
    room = models.ForeignKey(Room)
    qualifications = models.ManyToManyField(Qualification)
    length = NonZeroPositiveSmallIntegerField(help_text='in minutes')
    number_of_participants_needed = NonZeroPositiveSmallIntegerField(default=1, help_text='per slot')

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def already_signed_up(self, participant):
        return Appointment.objects.filter(slot__experiment_date_time_range__experiment_date__experiment=self,
                                          participant=participant).count() > 0

class ExperimentDate(models.Model):
    experiment = models.ForeignKey(Experiment)
    date = models.DateField(help_text='yyyy-mm-dd')

    class Meta:
        ordering = ('experiment', 'date',)
        unique_together = (('experiment', 'date',),)

    def __unicode__(self):
        return '%s on %s' % (self.experiment, self.date)

class ExperimentDateTimeRange(models.Model):
    experiment_date = models.ForeignKey(ExperimentDate)
    start_time = models.TimeField(help_text='hh:mm')
    end_time = models.TimeField(help_text='hh:mm')

    class Meta:
        ordering = ('experiment_date',)

    def __unicode__(self):
        return '%s from %s to %s' % (self.experiment_date, self.start_time, self.end_time)

    def create_slots(self):
        length = timedelta(minutes=self.experiment_date.experiment.length)
        date = self.experiment_date.date
        start_datetime = datetime.combine(date, self.start_time)
        end_datetime = datetime.combine(date, self.end_time)
        while start_datetime + length <= end_datetime:
            Slot.objects.create(experiment_date_time_range=self, start_time=start_datetime.time())
            start_datetime += length

class Slot(models.Model):
    experiment_date_time_range = models.ForeignKey(ExperimentDateTimeRange)
    start_time = models.TimeField()
    end_time = models.TimeField(editable=False) # start_time + experiment.length

    class Meta:
        ordering = ('experiment_date_time_range', 'start_time',)

    def __unicode__(self):
        return '%s from %s to %s' % (self.experiment_date_time_range.experiment_date, self.start_time, self.end_time)

    def save(self, *args, **kwargs):
        start_datetime = datetime.combine(self.experiment_date_time_range.experiment_date.date, self.start_time)
        end_datetime = start_datetime + timedelta(minutes=self.experiment_date_time_range.experiment_date.experiment.length)
        if start_datetime.date() != end_datetime.date():
            return
        self.end_time = end_datetime.time()
        super(Slot, self).save(*args, **kwargs)

    def is_in_past(self):
        return datetime.combine(self.experiment_date_time_range.experiment_date.date, self.start_time) < datetime.now()

    def is_full(self):
        return self.appointment_set.exclude(is_cancelled=True).count() == \
               self.experiment_date_time_range.experiment_date.experiment.number_of_participants_needed

    def is_conflicting_for(self, participant):
        return Slot.objects.filter(appointment__participant=participant,
                                   experiment_date_time_range__experiment_date__date=self.experiment_date_time_range.experiment_date.date,
                                   start_time__lt=self.end_time,
                                   end_time__gt=self.start_time).exclude(appointment__is_cancelled=True).count() > 0

class Appointment(models.Model):
    participant = models.ForeignKey(Participant)
    slot = models.ForeignKey(Slot)
    is_cancelled = models.BooleanField()

    class Meta:
        ordering = ('slot',)
        unique_together = (('participant', 'slot',),)

    def __unicode__(self):
        return '%s: %s' % (self.slot, self.participant)