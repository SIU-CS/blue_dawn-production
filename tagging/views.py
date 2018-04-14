from django.shortcuts import render
from templates import imported_libs
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

# display json data on a table
@login_required(login_url="/login")
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
