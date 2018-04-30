from django.shortcuts import render
from templates.JSONDataSet import JSONDataSet
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.encoding import smart_str

@login_required(login_url="/login")
def profile(request):
    data = list(map(lambda x: x.json_dict["title"], JSONDataSet.GetDatasets(request.user)))
    datasets = JSONDataSet.GetDatasets(request.user)
    username = request.user.username

    data = list()
    for d in datasets:
        temp = dict()
        temp['id'] = d.id
        temp['name'] = d.json_dict["title"]
        data.append(temp)

    return render(request,'profile.html', {"data": data, "username": username})

#deleting the whole dataset from the viewdata page
def deleteData(request):
    toreturn = dict()
    #get the dataset by "id" by passing the dataset's id to the "GetDataset" method in the JSONDataSet.py file
    dataset = JSONDataSet.GetDataset(request.POST.get("itemId"))
    #after getting the desired dataset, it passed to DeleteDataSet method in the the JSONDataSet.py file
    dataset.DeleteDataSet(request.user)
    toreturn["results"] = True
    
    return JsonResponse(toreturn)

