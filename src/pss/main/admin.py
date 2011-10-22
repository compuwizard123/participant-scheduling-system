from django.contrib import admin

from pss.main.models import Appointment, Building, Experiment, Participant, Qualification, Researcher, Room, Slot

admin.site.register(Appointment)
admin.site.register(Building)
admin.site.register(Experiment)
admin.site.register(Participant)
admin.site.register(Qualification)
admin.site.register(Researcher)
admin.site.register(Room)
admin.site.register(Slot)

# to-do: Actually make a good admin; don't just use the defaults.