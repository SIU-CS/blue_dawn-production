from django.shortcuts import render
from django.views import generic
from django.template import RequestContext
from django.views.generic.edit import CreateView, UpdateView
from .form import FileForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from landing.JSONDataSet import JSONDataSet
from landing.JSONDataSet import FileType
from landing.JSONDataSet import InputException
from django.core.files.storage import default_storage
from django.conf import settings
import os
import json
from .models import DataSet
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text, smart_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .form import RegistrationForm
from .tokens import accountActivation
from django.core.mail import EmailMessage
from django.core.files import File
from django.contrib.auth.decorators import login_required
from pprint import pprint
from django.http import JsonResponse


def index(request):
	return render(request,'index.html')

def login(request):
	return render(request,'login.html')

@login_required(login_url="/login")
def profile(request):
	data = list(map(lambda x: x.json_dict["title"], JSONDataSet.GetDatasets(request.user)))
	datasets = JSONDataSet.GetDatasets(request.user)
	username = request.user.username

	data = list()
	for d in datasets:
		temp = dict()
		temp['id'] = d.id
		temp['name'] = d.json_dict["title"]
		data.append(temp)

	return render(request,'profile.html', {"data": data, "username": username})

def wiki(request):
	return render(request,'wiki.html')

def importing(request):
	form = FileForm(request.POST or None)
	if request.method == 'POST':
		form = FileForm(request.POST, request.FILES)
		if form.is_valid():
			f = request.FILES['file']
			# TODO: should probably get the file type in a better way than looking at the extension (similar to linux `file`?)
			# file exension really says nothing about the type
			if os.path.splitext(f.name)[1] == ".csv":
				filetype = FileType.CSV
			elif os.path.splitext(f.name)[1] == ".xlsx":
				filetype = FileType.XLSX
			else:
				# TODO: correct way to error out here?
				return render(request, 'importing.html', { 'form': form })

			filepath = saveUploadedFile(f) # save file to disk temporarily

			name = request.POST.get("name", "")
			description = request.POST.get("description", "")

			try:
				data = JSONDataSet(filepath, filetype, name, description)
				data.SaveDataset(request.user) # save dataset to database as json
			except InputException:
				# TODO: correct way to error out here?
				os.remove(filepath) # delete the temporary file
				return render(request, 'importing.html')

			os.remove(filepath) # delete the temporary file

			data = list(map(lambda x: x.json_dict["title"], JSONDataSet.GetDatasets(request.user)))
			datasets = JSONDataSet.GetDatasets(request.user)
			username = request.user.username

			data = list()
			for d in datasets:
				temp = dict()
				temp['id'] = d.id
				temp['name'] = d.json_dict["title"]
				data.append(temp)

			return render(request,'profile.html', {"data": data, "username": username})

	return render(request, 'importing.html', { 'form': form })


# save an InMemoryUploadedFile to disk
# should this be in this file?
def saveUploadedFile(fpntr):
	with default_storage.open("tmp/" + fpntr.name, 'wb+') as destination:
		for chunk in fpntr.chunks():
			destination.write(chunk)

	return settings.MEDIA_ROOT + "/tmp/" + fpntr.name

# display json data on a table
def viewdata(request):
    parameter = request.GET.get('dataset', '')
    if (parameter != ""):
        id = parameter.split('-', 1)[1]
        data = JSONDataSet.GetDataset(id).json_dict['data']
        tags = JSONDataSet.GetDataset(id).json_dict['tags']
    else:
        data = None

    context = {
        'data': data,
        'tags': tags,
        'id': id,
    }

    return render(request, 'viewdata.html', context)

def addtag(request):
    toreturn = dict()
    try:
        dataset = JSONDataSet.GetDataset(request.POST.get("id"))

        if (dataset.HasTag(request.POST.get("tag"))):
            toreturn['results'] = False
            toreturn['message'] = "Tag already exists"
        else:
            dataset.AddTag(request.POST.get('tag'))
            dataset.SaveDataset(request.user)
            toreturn['results']=True

    except Exception as e:
        toreturn['results']=False
        toreturn['message']=str(e)
    return JsonResponse(toreturn)

def TagItem(request):
    toreturn = dict()

    try:
        dataset = JSONDataSet.GetDataset(request.POST.get("datasetId"))
        if (dataset.ItemHasTag(request.POST.get("itemId"), request.POST.getlist('tags[]')[-1])):
            toreturn['result'] = False
            toreturn['message'] = "Item already has that tag"
        else:
            dataset.TagItem(request.POST.get("itemId"), request.POST.getlist("tags[]"))
            dataset.SaveDataset(request.user)
            toreturn["result"] = True
    except Exception as e:
        toreturn['result'] = False
        toreturn['message'] = str(e)
    return JsonResponse(toreturn);

def ExportCSV(request):
    dataset = JSONDataSet.GetDataset(request.GET.get('id'))
    dataset.ExportCSV(request.user)

    file_name = dataset.json_dict['title'] + ".csv"
    fpntr = File(open("media/tmp/" + file_name))

    response = HttpResponse(fpntr, content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)

    os.remove("media/tmp/" + file_name)
    
    return response

def ExportXLSX(request):
    dataset = JSONDataSet.GetDataset(request.GET.get('id'))
    dataset.ExportXLSX(request.user)

    file_name = dataset.json_dict['title'] + ".xlsx"
    fpntr = File(open("media/tmp/" + file_name, 'rb'))

    response = HttpResponse(fpntr, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)

    os.remove("media/tmp/" + file_name)

    return response

def removetag(request):
    toreturn = dict()
    try:
        dataset = JSONDataSet.GetDataset(request.POST.get("id"))
        dataset.RemoveTag(request.POST.get("tag"))
        dataset.SaveDataset(request.user)
        toreturn["results"] = True
    except Exception as e:
        toreturn['results'] = False
        toreturn['message'] = str(e)

    return JsonResponse(toreturn)

def signup(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			current_site = get_current_site(request)
			subject = 'Activate you account'
			message = render_to_string('email_activation.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
				'token': accountActivation.make_token(user),
			})
			to_email = form.cleaned_data.get('email')
			email = EmailMessage(
						subject, message, to=[to_email]
			)
			email.send()
			return redirect('email_activation_sent')
	else:
		form = RegistrationForm()
	return render(request, 'signup.html', {'form': form})

def email_activation_sent(request):
	return render(request, 'email_activation_sent.html')


def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user is not None and accountActivation.check_token(user, token):
		user.is_active = True
		user.confirm.confirmation = True
		user.save()
		login(request)
		return redirect('activation_complete')
	else:
		return render(request, 'signup.html')

def activation_complete(request):
	return render(request, 'activation_complete.html')
