from django.shortcuts import render
from templates.JSONDataSet import JSONDataSet

def colSelect(request):
    parameter = request.GET.get('dataset', '')
    if parameter != "":
        dataset = JSONDataSet.GetDataset(parameter)
    else:
        return render(request,'index.html')

    questions = dataset.GetQuestions()
    context = {
        'questions': questions
    }
    return render(request, 'colSelect.html', context)
