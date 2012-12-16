from django.conf.urls import patterns, url

urlpatterns = patterns('transaction.api.views',
    url(r'^credit-points/$', 'credit_points'),
    url(r'^query-points/$', 'query_points'),
    url(r'^debit-points/$', 'debit_points'),
)
