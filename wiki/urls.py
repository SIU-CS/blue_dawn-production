"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from wiki import views

urlpatterns = [
    url(r'^$', views.wiki, name="wiki"),
    url(r'^accounts$', views.wiki_accounts, name="wiki_accounts"),
    url(r'^importing$', views.wiki_importing, name="wiki_importing"),
    url(r'^tagging$', views.wiki_tagging, name="wiki_tagging"),
    url(r'^exporting$', views.wiki_exporting, name="wiki_exporting"),
    url(r'^hosting$', views.wiki_hosting, name="wiki_hosting"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
