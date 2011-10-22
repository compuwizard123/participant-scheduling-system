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
    description = models.TextField()

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

class Experiment(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    researchers = models.ManyToManyField(Researcher)
    room = models.ForeignKey(Room)
    qualifications = models.ManyToManyField(Qualification)
    length = models.PositiveSmallIntegerField(help_text='in minutes') # to-do: > 0

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

class Slot(models.Model):
    experiment = models.ForeignKey(Experiment)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(editable=False) # start_time + experiment.length

    class Meta:
        ordering = ('experiment', 'date', 'start_time',)

    def __unicode__(self):
        return '%s on %s from %s to %s' % (self.experiment, self.date, self.start_time, self.end_time)

    def save(self, *args, **kwargs):
        start_datetime = datetime.combine(self.date, self.start_time)
        end_datetime = start_datetime + timedelta(minutes=self.experiment.length)
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