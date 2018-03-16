from django.shortcuts import render
from django.views import generic
from django.template import RequestContext
from django.views.generic.edit import CreateView
from .models import DataFile
from django.http import HttpResponseRedirect
from .form import FileForm
import csv
import untangle
import dicttoxml


def index(request):
	return render(request,'index.html')


#class ImportData(CreateView):
#	model = DataFile
#	fields = ['title', 'description', 'file']
	 #template_name = 'import.html'
	#return render(request,'import.html')

def login(request):
	return render(request,'login_page_index.html')
	
def userprofile(request):
	return render(request,'user_page_index.html')

def viewdata(request):
	return render(request,'view_data_page_index.html')

def importing(request):
	form = FileForm(request.POST or None)
	if request.method == 'POST':
		form = FileForm(request.POST, request.FILES)
		if form.is_valid():
			handle_upload_file(request.FILES['file'], request.FILES['file'].name)
			return HttpResponseRedirect('http://127.0.0.1:8000')
		
	return render(request, 'import.html', { 'form': form })


def handle_upload_file(f, n):
	xml = dicttoxml.dicttoxml(f)
	with open('media/'+ n + '.xml', 'wb+') as dest:
		dest.write(xml)


	
 


