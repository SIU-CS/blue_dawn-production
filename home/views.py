from django.shortcuts import render
from templates import imported_libs

def index(request):
	return render(request,'index.html')