from django.shortcuts import render

def wiki(request):
        return render(request,'wiki.html')

def wiki_accounts(request):
        return render(request, 'wiki_accounts.html')

def wiki_selecting(request):
        return render(request, 'wiki_selecting.html')

def wiki_importing(request):
        return render(request, 'wiki_importing.html')

def wiki_exporting(request):
        return render(request, 'wiki_exporting.html')

def wiki_creating_adding_tags(request):
        return render(request, 'wiki_creating_adding_tags.html')