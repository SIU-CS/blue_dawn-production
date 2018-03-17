from django.shortcuts import render
from django.views import generic
from django.template import RequestContext
from django.views.generic.edit import CreateView
from .models import DataFile
from .form import FileForm
from django.http import HttpResponseRedirect
from landing.JSONDataSet import JSONDataSet
from landing.JSONDataSet import FileType
from pprint import pprint
import os

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

#def dataimport(request):
#	return render(request, 'landing/datafile_form.html')

def importing(request):
	form = FileForm(request.POST or None)
	if request.method == 'POST':
		form = FileForm(request.POST, request.FILES)
		if form.is_valid():
			initial_obj = form.save(commit=False)
			initial_obj.save()
			f = request.FILES['file']
			filetype = os.path.splitext(f.name)[1]
			filepath = initial_obj.file.url
			#print(path)
			#print(ext)
			form.save()
			#def pass2json(self):
			JSONDataSet.__init__(filepath, filetype)
			return HttpResponseRedirect('http://127.0.0.1:8000')
		
	return render(request, 'landing/datafile_form.html', { 'form': form })