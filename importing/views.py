from django.shortcuts import render
from templates import imported_libs
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic
from django.template import RequestContext
from django.views.generic.edit import CreateView, UpdateView
from templates.form import FileForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from templates.JSONDataSet import JSONDataSet
from templates.JSONDataSet import FileType
from templates.JSONDataSet import InputException
from django.core.files.storage import default_storage
from django.conf import settings
import os
import json
from templates.models import DataSet
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text, smart_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from templates.form import RegistrationForm
from login.tokens import accountActivation
from django.core.mail import EmailMessage
from django.core.files import File
from django.contrib.auth.decorators import login_required
from pprint import pprint
from django.http import JsonResponse

@login_required(login_url="/login")
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