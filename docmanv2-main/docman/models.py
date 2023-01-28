from django.db import models
from django.contrib.auth.models import User
import datetime


class Event(models.Model):
	'''Conference, Symposium, or whatever event'''

	def __str__(self):
		return self.name

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = 'Event'
		verbose_name_plural  = 'Global event setup'



	slug = models.CharField(max_length=512, default=datetime.datetime.now())

	name				= models.CharField(max_length=256)
	description	= models.TextField(max_length=1024, null=True, blank=True)
	notes				= models.TextField(max_length=1024, null=True, blank=True)

	admins			= models.ManyToManyField(User, related_name='admin_events', blank=True)
	presenters	= models.ManyToManyField(User, related_name='presenter_events', blank=True)

	days				= models.ManyToManyField('Event_day', blank=True)
	rooms				= models.ManyToManyField('Room', related_name='event_rooms', blank=True)

class Event_day(models.Model):
	
	def __str__(self):
		return self.name

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = 'Event Day'
		verbose_name_plural  = 'Event Days'


	date					= models.DateField()
	name					= models.CharField(max_length=256)
	presentations = models.ManyToManyField('Presentation', blank=True)
	sessions			= models.ManyToManyField('Event_session', blank=True)
	slug = models.CharField(max_length=512, default=datetime.datetime.now())

	ordering_id		= models.IntegerField(default=0)


class Room(models.Model):
	
	def __str__(self):
		return self.name
	
	def __unicode__(self):
		return self.name
	class Meta:
		verbose_name = 'Room'
		verbose_name_plural  = 'Event Rooms'

	name				= models.CharField(max_length=256)
	description	= models.TextField(max_length=1024, null=True, blank=True)
	notes				= models.TextField(max_length=1024, null=True, blank=True)
	slug = models.CharField(max_length=512, default=datetime.datetime.now())

	ordering_id		= models.IntegerField(default=0)

class Event_session(models.Model):
	'''"Sessions" are groupings of presentations'''

	def __str__(self):
		return self.name

	def __unicode__(self):
		return self.name
	class Meta:
		verbose_name = 'Session'
		verbose_name_plural  = 'Sessions'

	name				= models.CharField(max_length=256)
	session_type= models.CharField(max_length=256, null=True, blank=True)
	description	= models.TextField(max_length=1024, null=True, blank=True)
	notes				= models.TextField(max_length=2048, null=True, blank=True)
	slug 				= models.CharField(max_length=512, default=datetime.datetime.now())
	room				= models.ForeignKey('Room', on_delete=models.CASCADE, null=True)

	start_time	= models.DateTimeField()
	end_time		= models.DateTimeField()

	ordering_id		= models.IntegerField(default=0)

class Presentation(models.Model):
	'''A presentation represents a single individual standing up and showing something
	It may include multiple documents.
	It must have either a start/stop time, OR be linked to a Session which has a start/stop time.
	'''
	def __str__(self):
		return self.name
	
	class Meta():
		ordering = ['presenter__last_name']


	def __unicode__(self):
		return self.name + ' ('+self.presenter.last_name+', '+self.presenter.first_name+')'
	name							= models.CharField(max_length=256)
	presenation_type	= models.CharField(max_length=256, null=True, blank=True)
	description				= models.TextField(max_length=1024, null=True, blank=True)
	notes							= models.TextField(max_length=1024, null=True, blank=True)
	slug 							= models.CharField(max_length=512, default=datetime.datetime.now())
	ordering_id				= models.IntegerField(default=0)
	room							= models.ForeignKey('Room', on_delete=models.CASCADE, null=True)

	presenter					= models.ForeignKey(User, on_delete=models.CASCADE)
	
# presentations can either have a time, or be linked to a session instead.
	start_time	= models.DateTimeField(null=True, blank=True)
	end_time		= models.DateTimeField(null=True, blank=True)
	session			= models.ForeignKey(Event_session, on_delete=models.CASCADE,  null=True, blank=True)

	documents		= models.ManyToManyField('Document', null=True, blank=True)

class Document(models.Model):
	'''powerpoint file, text document, whatever.

	'''
	def __str__(self):
		return self.name


	def __unicode__(self):
		return self.name
	name				= models.CharField(max_length=256)
	notes				= models.TextField(max_length=1024, null=True, blank=True)
	permitted_users = models.ManyToManyField(User, null=True)

	slug = models.CharField(max_length=512, default=datetime.datetime.now())
	is_deleted	= models.BooleanField(default=False)
	ordering_id		= models.IntegerField(default=0)

	latest_revision	= models.DateTimeField(auto_now_add=True)
	file_path = models.CharField('Relative local path and filename.', max_length=2048, null=True, blank=True)
	url = models.URLField('Full URL to an off-site shared resource.', max_length=2048, null=True, blank=True)
	preview_file_path = models.CharField('Relative local path to pre-generated preview image.', max_length=2048, null=True, blank=True)


class UserProfile(models.Model):
	'''Custom user account model.  Mapped to a django user account for login management.
	'''
	def __str__(self):
		return self.user.last_name+', '+self.user.first_name

	def __unicode__(self):
		return self.user.last_name+', '+self.user.first_name
	user			= models.OneToOneField(User, on_delete=models.CASCADE,  unique=True)
	password	= models.CharField(max_length=16, blank=True)

	title			= models.CharField(max_length=1024, blank=True)
	company		= models.CharField(max_length=128, blank=True)

	is_admin	= models.BooleanField(default=False)
	read_only_admin = models.BooleanField(default=False)


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

