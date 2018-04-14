from django.shortcuts import render
from templates.JSONDataSet import JSONDataSet
from django.contrib.auth.decorators import login_required
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
