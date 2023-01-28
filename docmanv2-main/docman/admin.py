from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models
from docman.models import Event, Event_day, Room, Event_session, Presentation, Document, UserProfile
from django.contrib.auth.models import Group


class Event_sessionAdmin(admin.ModelAdmin):
	date_hierarchy = 'start_time'
	actions_on_bottom = True
	actions_on_top = False
	list_display = ('name', 'room', 'start_time')
	list_filter = ('room',)
	exclude = ('session_type', 'slug', 'ordering_id')
	fields = (('name', 'room'), ('start_time', 'end_time'), 'description', 'notes')
	ordering = ['start_time', 'room']
	search_fields = ['name', 'room__name', 'description', 'notes']

	def view_on_site(self, obj):
		event_day = Event_day.objects.get(date__day=obj.start_time.day)
		return '/calendar/'+event_day.name+'#'+obj.room.name

class PresentationAdmin(admin.ModelAdmin):
	search_fields = ['name', 'room__name', 'description', 'notes', 'presenter__email', 'presenter__first_name', 'presenter__last_name', 'session__name']
	list_display = ('name', 'presenter', 'room', 'session' )
	actions_on_bottom = True
	actions_on_top = False
	fields = ('name', 'room', 'presenter', 'session', 'description', 'notes')

	formfield_overrides = {
		models.CharField: {'widget': TextInput(attrs={'size':'100'})},
	}

admin.site.site_header = 'DocMan Administration'
admin.site.site_title = 'DocMan Admin'
admin.site.index_title = 'Event Setup and Management'


admin.site.register(Event)
admin.site.register(Event_day)
admin.site.register(Room)
admin.site.register(Event_session, Event_sessionAdmin)
admin.site.register(Presentation, PresentationAdmin)
admin.site.register(Document)
admin.site.register(UserProfile)
#admin.site.unregister(Group)
