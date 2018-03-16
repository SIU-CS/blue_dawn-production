from django.shortcuts import render
from django.views import generic
from django.template import RequestContext
from django.views.generic.edit import CreateView
#from .models import DataFile
from landing.JSONDataSet import JSONDataSet
from landing.JSONDataSet import FileType

from pprint import pprint

def index(request):
    d = JSONDataSet("/home/michael/Desktop/csv.csv", FileType.CSV)
    pprint(d.json_dict)

    d.AddTag("TAG1")
    pprint(d.json_dict)
    d.AddTag("TAG2")
    pprint(d.json_dict)

    d.SaveDataset(request.user)

    return render(request,'index.html')


class ImportData(CreateView):
#	model = DataFile
	fields = ['title', 'description', 'file']
        
	 #template_name = 'import.html'
	#return render(request,'import.html')

def login(request):
	return render(request,'login_page_index.html')
	
def userprofile(request):
	return render(request,'user_page_index.html')

def viewdata(request):
	return render(request,'view_data_page_index.html')
