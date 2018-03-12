from django.shortcuts import render
from django.views import generic
from django.template import RequestContext
from django.views.generic.edit import CreateView
from .models import DataFile

def index(request):
    return render(request,'index.html')


class ImportData(CreateView):
	model = DataFile
	fields = ['title', 'description', 'file']
	 #template_name = 'import.html'
	#return render(request,'import.html')

def login(request):
	return render(request,'login_page_index.html')
	
	

