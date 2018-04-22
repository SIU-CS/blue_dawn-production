from django.shortcuts import render
from templates.JSONDataSet import JSONDataSet
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files import File
from django.http import HttpResponse
from django.utils.encoding import smart_str
from pprint import pprint
import os

# display json data on a table
@login_required(login_url="/login")
def viewdata(request):
    parameter = request.GET.get('dataset', '')
    if (parameter != ""):
        id = parameter.split('-', 1)[1]
        dataset = JSONDataSet.GetDataset(id)
    else:
        return render(request,'index.html')

    context = {
        'data': dataset.GetResponseMatrix(),
        'questions': dataset.GetQuestions(),
        'tags': dataset.GetTags(),
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
        if (dataset.ItemHasTag(request.POST.get("rid"), request.POST.getlist('tags[]')[-1])):
            toreturn['result'] = False
            toreturn['message'] = "Item already has that tag"
        else:
            dataset.TagItem(request.POST.get("rid"), request.POST.getlist("tags[]"))
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
