from django.shortcuts import render
from django.views import generic
from django.template import RequestContext
from django.views.generic.edit import CreateView, UpdateView
from .form import FileForm
from django.http import HttpResponseRedirect
from landing.JSONDataSet import JSONDataSet
from landing.JSONDataSet import FileType
from landing.JSONDataSet import InputException
from django.core.files.storage import default_storage
from django.conf import settings
import os
import json
from .models import DataSet
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .form import RegistrationForm
from .tokens import accountActivation

def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'login.html')
	
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

# dispaly json data on a table
def viewdata(request):
    parameter = request.GET.get('dataset', '')
    if (parameter != ""):
        id = parameter.split('-', 1)[1]
        data = JSONDataSet.GetDataset(id).json_dict['data']
    else:
        data = None

    context = {
        'data': data,
    }

    return render(request, 'viewdata.html', context)

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
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('email_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def email_activation_sent(request):
    return render(request, 'email_activation.html')


