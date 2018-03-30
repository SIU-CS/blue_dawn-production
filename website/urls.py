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
from landing import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout



urlpatterns = [
	path('', views.index, name='index'),
	path('admin/', admin.site.urls),
	url(r'^importing$', views.importing, name='importing'),
	#url(r'^login$', views.login, name='login'),
	url(r'^login/$', auth_views.login, name='login'),
	url(r'^accounts/profile/$', views.profile, name='profile'),
	url(r'^viewdata$', views.viewdata, name='viewdata'),
	url(r'^wiki$', views.wiki, name="wiki"),
	url(r'^signup$', views.signup, name ="signup"),
	url(r'^email_activation_sent/$', views.email_activation_sent, name='email_activation_sent'),
	url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
	url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^activation_complete/$', views.activation_complete, name= 'activation_complete'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout')

]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

