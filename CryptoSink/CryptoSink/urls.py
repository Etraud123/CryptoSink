from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponse
from cryptoclient import views
#from core import *
from django.conf import settings
from django.conf.urls.static import static

 
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CryptoSink.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^core/', 'core.views.home', name='home'),
    url(r'^login/', 'core.views.login', name='login'),
    url(r'^register/', 'core.views.register', name='register'),
 
    #url(r'^core/', include('core.urls')),
    url(r'.*media/(?P<path>.*)', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
    url(r'.*css/(?P<path>.*)', 'django.views.static.serve', {'document_root': settings.THEMES_ROOT,}),
    url(r'.*img/(?P<path>.*)', 'django.views.static.serve', {'document_root': settings.IMAGES_ROOT,}),
    url(r'.*js/(?P<path>.*)', 'django.views.static.serve', {'document_root': settings.SCRIPTS_ROOT,}),
    url(r'.*fonts/(?P<path>.*)', 'django.views.static.serve', {'document_root': settings.FONTS_ROOT,}),
    url(r'.*files/(?P<path>.*)', 'django.views.static.serve', {'document_root': settings.FILES_ROOT,}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'cryptoclient.views.home', name='home'),
    url(r'^logout/', 'cryptoclient.views.logout_user', name='logout'),
    url(r'^upload/', 'cryptoclient.views.upload_user', name='upload'),
    url(r'^upload_file/', 'cryptoclient.views.upload_file', name='upload_file'),
    url(r'^download_file/', 'cryptoclient.views.download_file', name='download_file'),


)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
