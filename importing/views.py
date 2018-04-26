from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from templates.form import FileForm
from django.core.files.storage import default_storage
from django.conf import settings
from templates.JSONDataSet import JSONDataSet, FileType, InputException
import os

@login_required(login_url="/login")
def importing(request):
    form = FileForm(request.POST or None)
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            # TODO: should probably get the file type in a better way than looking at the extension (similar to linux `file`?)
            # file exension really says nothing about the type
            if os.path.splitext(f.name)[1] == ".csv":
                filetype = FileType.CSV
            elif os.path.splitext(f.name)[1] == ".xlsx":
                filetype = FileType.XLSX
            else:
                # TODO: correct way to error out here?
                return render(request, 'importing.html', { 'form': form })

            filepath = saveUploadedFile(f) # save file to disk temporarily

            name = request.POST.get("name", "")
            description = request.POST.get("description", "")

            try:
                data = JSONDataSet(filepath, filetype, name, description)
                data.SaveDataset(request.user) # save dataset to database as json
            except InputException:
                # TODO: correct way to error out here?
                os.remove(filepath) # delete the temporary file
                return render(request, 'importing.html')

            os.remove(filepath) # delete the temporary file

            data = list(map(lambda x: x.json_dict["title"], JSONDataSet.GetDatasets(request.user)))
            datasets = JSONDataSet.GetDatasets(request.user)
            username = request.user.username

            data = list()
            for d in datasets:
                temp = dict()
                temp['id'] = d.id
                temp['name'] = d.json_dict["title"]
                data.append(temp)

            return redirect('http://127.0.0.1:8000/userpage/')

    return render(request, 'importing.html', { 'form': form })


# save an InMemoryUploadedFile to disk
# should this be in this file?
def saveUploadedFile(fpntr):
    with default_storage.open("tmp/" + fpntr.name, 'wb+') as destination:
        for chunk in fpntr.chunks():
            destination.write(chunk)

    return settings.MEDIA_ROOT + "/tmp/" + fpntr.name
