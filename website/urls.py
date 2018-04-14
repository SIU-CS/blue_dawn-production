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
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from home import views as home_views
from importing import views as importing_views
from login import views as login_views
from tagging import views as tagging_views
from templates import views as templates_views
from userpage import views as userpage_views
from wiki import views as wiki_views


urlpatterns = [
    path('', home_views.index, name='index'),
    path('admin/', admin.site.urls),
    url(r'^importing$', importing_views.importing, name='importing'),
    #url(r'^login$', views.login, name='login'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^accounts/profile/$', userpage_views.profile, name='profile'),
    url(r'^viewdata$', tagging_views.viewdata, name='viewdata'),
    url(r'^wiki$', wiki_views.wiki, name="wiki"),
    url(r'^signup$', login_views.signup, name ="signup"),
    url(r'^email_activation_sent/$', login_views.email_activation_sent, name='email_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', login_views.activate, name='activate'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^activation_complete/$', login_views.activation_complete, name= 'activation_complete'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^viewdata/addtag$', tagging_views.addtag, name='addtag'),
    url(r'^viewdata/removetag$', tagging_views.removetag, name='removetag'),
    url(r'^viewdata/TagItem$', tagging_views.TagItem, name='TagItem'),
    url(r'^viewdata/ExportCSV$', templates_views.ExportCSV, name='ExportCSV'),
    url(r'^viewdata/ExportXLSX$', templates_views.ExportXLSX, name='ExportXLSX')

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
