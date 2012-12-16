from django.conf.urls import patterns, url

urlpatterns = patterns('account.views',
    url(r'^signin/$', 'signin', name='signin'),
    url(r'^signup/$', 'signup', name='signup'),
    url(r'^account/$', 'account', name='account'),
)

urlpatterns += patterns('',
    url(r'^signout/$', 'django.contrib.auth.views.logout_then_login',
        name='signout'),
)
