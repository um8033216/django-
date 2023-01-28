from email import message
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os, time
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.template import RequestContext
from django.utils.text import slugify
from django.db.models import Q
import json
from docman.models import Event, Event_day, Room, Event_session, Presentation, Document, UserProfile
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView

UPLOAD_FOLDER = 'media/'
DELETE_URL = '/delete_files/'




def template(request):

	response_dict = {}

	response_dict['event'] = Event.objects.all()

	return render(request, "docman/template.html", response_dict)


def about(request):
    return render(request, "docman/about.html")

def contact(request):
    return render(request, "docman/contact.html")


def presentation_view_no_upload(request, pres_id):

	response_dict = {}

#	try:
	pres = Presentation.objects.get(id=pres_id)
#	except:
#		pres = Presentation()
#		pres.room = Room.objects.all()[0]
#		pres.presenter = request.user
#		pres.session = Event_session.objects.all()[0]
#		pres.save()
	
#	if request.user == pres.presenter or request.user.is_staff or request.user.is_superuser:
#		pass
#	else:
#		return HttpResponseForbidden()

	response_dict['presentation'] = pres


	return render(request, 'docman/presentation_view_no_upload.html', response_dict)

def presentation_view(request, pres_id):

	response_dict = {}

#	try:
	pres = Presentation.objects.get(id=pres_id)
	emessage = "Hello, we haven't received your document yet!" 
#	except:
#		pres = Presentation()
#		pres.room = Room.objects.all()[0]
#		pres.presenter = request.user
#		pres.session = Event_session.objects.all()[0]
#		pres.save()
	
	if request.user == pres.presenter or request.user.is_staff or request.user.is_superuser:
		pass
	else:
		return HttpResponseForbidden()

	response_dict['presentation'] = pres
	response_dict['message'] = emessage

	
	if request.user.is_staff or request.user.is_superuser:
		if request.method == 'POST' and 'sendemail' in request.POST:
			send_email(request, pres.presenter.username)
			response_dict['alert'] = '<li class="text-center" id="alert" style="color:red;""> <h1>Email Sent!</h1></li>'
			return render(request, 'docman/presentation_view.html', response_dict)

	return render(request, 'docman/presentation_view.html', response_dict)

@login_required
def send_email(request, toemail):
	#    subject = request.POST.get('subject', '')
	#    message = request.POST.get('message', '')
	#    from_email = request.POST.get('from_email', '')
		subject = "Reminder: Upload your document to CoDoMa"
		message = "Hello, we haven't received your document yet!"
		request.session['emessage'] = message
		from_email = "chris.albert@isilive.ca"
		if subject and message and from_email:
			try:
				send_mail(subject, message, from_email, [toemail], fail_silently=False)
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
		else:
			# In reality we'd use a form class
			# to get proper validation errors.
			return HttpResponse('Make sure all fields are entered and valid.')	

@login_required
def manage_files(request):


	response_dict = {'files':[]}

	presentation_id = request.META.get('HTTP_REFERER').split('/')[-1]
	presentation = Presentation.objects.get(id=presentation_id)

	upload_folder = UPLOAD_FOLDER + presentation_id + '/'

	if request.user.profile.read_only_admin == False:
	#if True:
		# read-only admin accounts may not upload files

		if not os.path.exists(upload_folder):
			os.makedirs(upload_folder)

		for x in request.FILES.values():
			filename = upload_folder+x.name
			filename = filename.encode('utf-8')
			open(filename, 'wb').write(x.read())
			#generate_preview(upload_folder+x.name)
			new_file_info = {
				'name':x.name,
				'size':os.path.getsize(filename),
				'time':time.ctime(os.path.getmtime(filename)),
#				'url':'http://docman.isiglobal.ca/files/'+presentation_id+'/'+x.name,
				'url':'/files/'+presentation_id+'/'+x.name,
				#'thumbnailUrl':'http://docman.isiglobal.ca/static/img/'+presentation_id+'/'+x.name+'-preview.png',
				'thumbnailUrl':'/static/img/document-preview.gif',
				'deleteUrl':DELETE_URL+presentation_id+'/'+x.name,
				'deleteType':'POST'	}
			response_dict['files'].append(new_file_info)

			# register the uploaded file in the database
			new_doc = Document()
			new_doc.slug = slugify(x.name)
			new_doc.name = x.name
			new_doc.file_path = presentation_id+'/'+x.name
			new_doc.preview_file_path = presentation_id+'/'+x.name+'-preview.png'
			new_doc.save()

			presentation.documents.add(new_doc)
			presentation.save()

		# identify and note file type
#		base, extension = os.path.splitext(x.name)
#		extension = extension.lstrip('.').lower()
#		if extension in ['jpg', 'png', 'bmp', 'tga', 'jpeg', 'ico', 'gif', 'psd']: new_resource.file_type = 'image'
#		elif extension in ['avi', 'mp4', 'mpeg', 'mpg', 'vob', 'wmv', 'mkv']: new_resource.file_type = 'video'
#		elif extension in ['ppt', 'pptx', 'odp']: new_resource.file_type = 'ppt'
#		elif extension in ['doc', 'docx', 'odt']: new_resource.file_type = 'doc'
#		elif extension in ['xls', 'xlsx']: new_resource.file_type = 'spreadsheet'
		
#		new_resource.save()
		
#		item.resources.add(new_resource)
#		if not item.primary_file:
#			item.primary_file = new_resource
#		item.save()



	if not len(response_dict['files']):
		# no new files uploaded, provide a full file list
		for f in os.listdir(upload_folder):
			try:
				if f[-12:] == '-preview.png' or f[-12:] == 'ew-large.png': continue
			except:
				pass
			new_file_info = {
				'name':f,
				'size':os.path.getsize(upload_folder+f),
				'time':time.ctime(os.path.getmtime(upload_folder+f)),
				'url':'/files/'+presentation_id+'/'+f,
				#'thumbnailUrl':CONTENT_URL+presentation_id+'/'+f+'-preview.png',
				'thumbnailUrl':'/static/img/document-preview.gif',
				'deleteUrl':DELETE_URL+presentation_id+'/'+f,
				'deleteType':'POST'	}
			response_dict['files'].append(new_file_info)

	json_response = json.dumps(response_dict)
	return HttpResponse(json_response)

@login_required
def delete_files(request, pres_id, filename):
	if request.user.profile.read_only_admin == True:
		return HttpResponseForbidden()

	response_dict = {'files':[]}

#	presentation_id = request.META.get('HTTP_REFERER').split('/')[-1]
	presentation = Presentation.objects.get(id=pres_id)

	upload_folder = UPLOAD_FOLDER + pres_id + '/'

	try:
		encoded_filename = upload_folder+filename
		encoded_filename = encoded_filename.encode('utf-8')
		os.remove(encoded_filename)
		new_file_info = {	filename:'true' }
		Document.objects.filter(file_path=pres_id + '/'+filename).delete()

	except:
		new_file_info = {	filename:'false' }
	response_dict['files'].append(new_file_info)

	json_response = json.dumps(response_dict)
	return HttpResponse(json_response)

@login_required
def files(request, pres_id, filename):

	pres = Presentation.objects.get(id=pres_id)

#	if request.user == pres.presenter or request.user.is_staff or request.user.is_superuser:
#		pass
#	else:
#		return HttpResponseForbidden()

	data = open(UPLOAD_FOLDER+'/'+pres_id+'/'+filename, 'r', encoding="utf8").read()
	response = HttpResponse(data, content_type="application/octet-stream")
#vnd.ms-excel")
	response['Content-Disposition'] = 'attachment; filename="'+filename+'"'

	return response
	
@login_required
def calendar_view(request, day):

	response_dict = {}

	if not request.user.is_staff and not request.user.is_superuser:
		return HttpResponseForbidden()


	response_dict['event'] = Event.objects.all

	response_dict['rooms'] = Room.objects.all()
	response_dict['day'] = Event_day.objects.get( name=day )
	# need sessions with a date-day that matches the day's date-day.
	#response_dict['sessions'] = Event_session.objects.filter(start_time__day=day)
	sessions = {}
	for session in Event_session.objects.all():
		sessions[session.id] = session
	response_dict['sessions'] = sessions

	return render(request, 'docman/calendar_view_'+day+'.html', response_dict)
	

@login_required
def edit_user(request):
	# this is an RPC function

	response_dict = {}

	if not request.user.is_staff and not request.user.is_superuser:
		return HttpResponseForbidden()

	user = User.objects.get(email = request.POST['username'])

	user.username = request.POST['new_username'].lower()
	user.first_name = request.POST['first_name']
	user.last_name = request.POST['last_name']
	user.set_password(request.POST['password'])
	for event in user.presenter_events.all():
		user.presenter_events.remove(event)
	for event_id in request.POST.getlist('user_events'):
		user.presenter_events.add(Event.objects.get(id=int(event_id)))

	profile = user.profile
	profile.password = request.POST['password']
	profile.save()
	user.save()

	response_dict['message'] = 'Changes saved.'
	response_dict['username'] = user.username
	response_dict['first_name'] = user.first_name
	response_dict['last_name'] = user.last_name
	response_dict['password'] = profile.password

	return HttpResponse(json.dumps(response_dict), content_type="application/json")


#@login_required
def users(request):

	response_dict = {}

	if not request.user.is_staff and not request.user.is_superuser:
		return render(request, 'docman/message.html', {'message':'Access denied.  This page is only available to administrators.'})

#	if request.user.is_staff:
#		response_dict['events'] = request.user.admin_events.all()
#	else:
#		response_dict['events'] = Events.objects.all()

	if request.POST:
		# add user form has been submitted
		try:
			existing_user = User.objects.get(email = request.POST['new_username'])
			response_dict['username'] = request.POST['new_username'].lower()
			response_dict['password'] = request.POST['new_password']
			response_dict['new_first_name'] = request.POST['new_first_name']
			response_dict['new_last_name'] = request.POST['new_last_name']
			response_dict['user_error'] = 'has-error has-feedback'
			response_dict['error_message'] = 'A user with that address already exists!'
			return render(request, 'docman/users.html', response_dict)
		except:
			pass

#		event = Event.objects.get(id=request.POST['new_user_event'])

		new_user = User()
		new_user.username = request.POST['new_username'].lstrip().rstrip().lower()
		new_user.email = request.POST['new_username'].lstrip().rstrip().lower()
		new_user.set_password(request.POST['new_password'].lstrip().rstrip())
		new_user.first_name = request.POST['new_first_name'].lstrip().rstrip()
		new_user.last_name = request.POST['new_last_name'].lstrip().rstrip()
		new_user.save()
		new_profile = new_user.profile
		new_profile.password = request.POST['new_password'].lstrip().rstrip()
		new_profile.save()

#		event.presenters.add(new_user)
#		event.save()

		response_dict['message'] = 'New user '+new_user.email+' created.'



	return render(request, 'docman/users.html', response_dict)

@login_required
def users_csv(request):
	if not request.user.is_superuser:
		return HttpResponseForbidden()

	response_dict = {}

	# make a list of the events the user has admin rights on
#	if request.user.is_staff:
#		response_dict['events'] = request.user.admin_events.all()
#	else:
#		response_dict['events'] = Events.objects.all()

	# make a list of all the presenters associated with those events
#	q = Q()
#	for event in response_dict['events']:
#		q |= Q(presenter_events__id=event.id)
#	response_dict['users'] = User.objects.filter(q).order_by('username')
	response_dict['users'] = User.objects.all().order_by('username')

	csv = []
	for u in response_dict['users']:
		line = [u.username, u.profile.password, u.first_name, u.last_name]
		
		csv.append(','.join(line))
	
	return HttpResponse('<br>'.join(csv))
	
	# render an html snippet and return it for the javascript code to insert dynamically
#	return render('user_list.html', response_dict, context_instance=RequestContext(request))

@login_required
def users_rpc(request):
	if not request.user.is_staff and not request.user.is_superuser:
		return HttpResponseForbidden()

	response_dict = {}

	# make a list of the events the user has admin rights on
#	if request.user.is_staff:
#		response_dict['events'] = request.user.admin_events.all()
#	else:
#		response_dict['events'] = Events.objects.all()

	# make a list of all the presenters associated with those events
#	q = Q()
#	for event in response_dict['events']:
#		q |= Q(presenter_events__id=event.id)
#	response_dict['users'] = User.objects.filter(q)
	response_dict['users'] = User.objects.all()
	
	# render an html snippet and return it for the javascript code to insert dynamically
	return render(request, 'docman/user_list.html', response_dict)

@login_required
def events(request):
	response_dict = {}

	return render(request, 'docman/events.html', response_dict)


#@login_required
#def index(request):
#	return redirect('/calendar/1')
@login_required
def index(request):

	if request.user.is_staff or request.user.is_superuser:
		return redirect('/calendar/1')

	if len(request.user.presentation_set.all()) == 1:
		presentation = request.user.presentation_set.all()[0]
		return redirect('/presentation/'+str(presentation.id))
	else:
		response_dict = {'presentations':request.user.presentation_set.all()}
		return render(request, 'docman/presentation_select.html', response_dict)




def login_user(request):
	response_dict = {}
	username = password = ''
	if request.POST:
		username = request.POST.get('username')
		response_dict['username'] = username
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:

#			if not user.is_staff and not user.is_superuser:
#				return render('message.html', {'message':'The presentation submission deadline has passed.  Login is now restricted to administrators only.'}, context_instance=RequestContext(request))		

			if user.is_active:
				login(request, user)
				# login success!
				if request.POST.__contains__('next'):
					redirect_url = request.POST.get('next')
				else:
					redirect_url = '/'
				return redirect(redirect_url)
		else:
			try:
				user_exists = User.objects.get(username=username)
			except:
				response_dict['user_error'] = 'has-error has-feedback'
			else:
				response_dict['password_error'] = 'has-error has-feedback'

	return render(request,'docman/login.html', response_dict)


@login_required
def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/')

@login_required
def filelist(request):

	response_dict = {}

	if not request.user.is_staff and not request.user.is_superuser:
		return HttpResponseForbidden()

	response_dict['presentation'] = Presentation.objects.all()
	response_dict['rooms'] = Room.objects.all()
	# need sessions with a date-day that matches the day's date-day.
	#response_dict['sessions'] = Event_session.objects.filter(start_time__day=day)
	sessions = {}
	for session in Event_session.objects.all():
		sessions[session.id] = session
	response_dict['sessions'] = sessions

	return render(request, 'docman/filelist.html', response_dict)

