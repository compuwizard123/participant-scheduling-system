from django.contrib import admin

from pss.main.models import Appointment, Building, Experiment, Participant, Qualification, Researcher, Room, Slot

class AppointmentInline(admin.TabularInline):
    model = Appointment
    extra = 0

class RoomInline(admin.TabularInline):
    model = Room
    extra = 0

class SlotInline(admin.TabularInline):
    model = Slot
    extra = 0

class BuildingAdmin(admin.ModelAdmin):
    inlines = (RoomInline,)
    list_display = ('name',)
    search_fields = ('name',)

def researchers(obj):
    return ', '.join(map(unicode, obj.researchers.all()))

def qualifications(obj):
    return ', '.join(map(unicode, obj.qualifications.all()))

class ExperimentAdmin(admin.ModelAdmin):
    inlines = (SlotInline,)
    list_display = ('name', 'description', researchers, 'room', qualifications, 'length')
    search_fields = ('name', 'description',)

def name(obj):
    return unicode(obj)
name.short_description = 'Name'

def email(obj):
    return obj.user.email
email.short_description = 'E-mail address'

class ParticipantAdmin(admin.ModelAdmin):
    inlines = (AppointmentInline,)
    list_display = (name, email, 'phone_number',)
    search_fields = ('user__last_name', 'user__first_name', 'user__username',)

class ResearcherAdmin(admin.ModelAdmin):
    list_display = (name, email, 'phone_number',)
    search_fields = ('user__last_name', 'user__first_name', 'user__username',)

class QualificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ('name', 'description',)

admin.site.register(Building, BuildingAdmin)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Qualification, QualificationAdmin)
admin.site.register(Researcher, ResearcherAdmin)