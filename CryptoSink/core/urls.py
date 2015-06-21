from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'core.views.core', name='core'),
	
	#url(r'^profile/', 'madlabs.core.views.profile', name='profile'),
)
