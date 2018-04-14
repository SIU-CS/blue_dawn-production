from django.shortcuts import render
from django.http import HttpResponse
from templates.JSONDataSet import JSONDataSet
from django.core.files import File
from django.utils.encoding import smart_str
import os

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
