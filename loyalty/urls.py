from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^$', 'account.views.signin', name='home'),
    url(r'^account/', include('account.urls')),
    url(r'^404/$', direct_to_template, {'template': '404.html'}, name='404'),
    url(r'^500/$', direct_to_template, {'template': '500.html'}, name='500'),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
