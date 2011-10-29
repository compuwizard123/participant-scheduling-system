from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField
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
    description = models.TextField() # to-do: Required?

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

class Experiment(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField() # to-do: Required?
    researchers = models.ManyToManyField(Researcher)
    room = models.ForeignKey(Room)
    qualifications = models.ManyToManyField(Qualification) # to-do: Required?
    length = models.PositiveSmallIntegerField(help_text='in minutes') # to-do: > 0

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

class ExperimentDate(models.Model):
    experiment = models.ForeignKey(Experiment)
    date = models.DateField()

    class Meta:
        ordering = ('experiment', 'date',)
        unique_together = (('experiment', 'date',),)

    def __unicode__(self):
        return '%s on %s' % (self.experiment, self.date)

class ExperimentDateTimeRange(models.Model):
    experiment_date = models.ForeignKey(ExperimentDate)
    start_time = models.TimeField()
    end_time = models.TimeField()
    # to-do: start_time + experiment.length <= end_time
    # to-do: Make sure no two ExperimentDateTimeRanges for one ExperimentDate overlap.
    # to-do: Make sure there are no room conflicts.

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
        # to-do: What if start_datetime.date() != end_datetime.date()?
        self.end_time = end_datetime.time()
        super(Slot, self).save(*args, **kwargs)

class Appointment(models.Model):
    participant = models.ForeignKey(Participant)
    slot = models.ForeignKey(Slot)

    class Meta:
        ordering = ('slot',)
        unique_together = (('participant', 'slot',),)

    def __unicode__(self):
        return '%s: %s' % (self.slot, self.participant)