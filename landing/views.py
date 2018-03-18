from django.shortcuts import render
from django.views import generic
from django.template import RequestContext
from django.views.generic.edit import CreateView, UpdateView
from .form import FileForm
from django.http import HttpResponseRedirect
from landing.JSONDataSet import JSONDataSet
from landing.JSONDataSet import FileType
from pprint import pprint
from django.core.files.storage import default_storage
from django.conf import settings
import os
from .models import DataSet

def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'login_page_index.html')
	
def userprofile(request):
    return render(request,'user_page_index.html')

def viewdata(request):
    return render(request,'view_data_page_index.html')

def assigntag(request):
	return render(request,'assign_tag_page_index.html')

def wikimain(request):
    return render(request,'wiki-main.html')
  
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
                return render(request, 'landing/datafile_form.html', { 'form': form })

            filepath = saveUploadedFile(f) # save file to disk temporarily

            name = request.POST.get("name", "")
            description = request.POST.get("description", "")
            
            data = JSONDataSet(filepath, filetype, name, description)
            data.SaveDataset(request.user) # save dataset to database as json

            os.remove(filepath) # delete the temporary file

            return HttpResponseRedirect('http://127.0.0.1:8000')
		
    return render(request, 'landing/datafile_form.html', { 'form': form })


# save an InMemoryUploadedFile to disk
# should this be in this file?
def saveUploadedFile(fpntr):
    with default_storage.open("tmp/" + fpntr.name, 'wb+') as destination:
        for chunk in fpntr.chunks():
            destination.write(chunk)

    return settings.MEDIA_ROOT + "/tmp/" + fpntr.name

# dispaly json data on a table
def json2Table(request):
	allData = DataSet.objects.all()
	context = {
		'allData': allData,
	}
	return render(request, 'landing/viewData.html', context)


