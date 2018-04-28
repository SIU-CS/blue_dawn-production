from django.shortcuts import render

def wiki(request):
        return render(request,'wiki.html')

def wiki_accounts(request):
        return render(request, 'wiki_accounts.html')

def wiki_importing(request):
        return render(request, 'wiki_importing.html')

def wiki_exporting(request):
        return render(request, 'wiki_exporting.html')

def wiki_tagging(request):
        return render(request, 'wiki_tagging.html')

def wiki_hosting(request):
        return render(request, 'wiki_hosting.html')