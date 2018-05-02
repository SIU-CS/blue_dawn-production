from django.shortcuts import render
from templates.JSONDataSet import JSONDataSet
from django.http import JsonResponse

def colSelect(request):
    parameter = request.GET.get('dataset', '')
    if parameter != "":
        dataset = JSONDataSet.GetDataset(parameter)
    else:
        return render(request,'index.html')

    questions = dataset.GetQuestions(True)
    context = {
        'questions': questions,
        'id': parameter
    }
    return render(request, 'colSelect.html', context)

def setCols(request):
    toreturn = dict()
    try:
        dataset = JSONDataSet.GetDataset(request.POST.get('id'))
        dataset.SetCols(request.POST.getlist('cols[]'))
        dataset.SaveDataset(request.user)
        toreturn['result'] = True
    except Exception as e:
        toreturn['result'] = False
        toreturn['message'] = str(e)
    return JsonResponse(toreturn)
