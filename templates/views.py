from django.shortcuts import render
from templates import imported_libs
from django.shortcuts import render
from django.views import generic
from django.template import RequestContext
from django.views.generic.edit import CreateView, UpdateView
from .form import FileForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from templates.JSONDataSet import JSONDataSet
from templates.JSONDataSet import FileType
from templates.JSONDataSet import InputException
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
from login.tokens import accountActivation
from django.core.mail import EmailMessage
from django.core.files import File
from django.contrib.auth.decorators import login_required
from pprint import pprint
from django.http import JsonResponse

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