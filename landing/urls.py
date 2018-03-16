from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'data/import', views.ImportData.as_view(), name='data-import'),
    url(r'login', views.login, name='login'),
    url(r'importing', views.importing.as_view(), name='importing'),
]

