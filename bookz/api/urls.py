from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^import_by_isbn/(?P<apikey>\w+)/(?P<isbn>\w+)/$', 'api.views.import_by_isbn'),
    url(r'^mark_as_owned/(?P<apikey>\w+)/(?P<isbn>\w+)/$', 'api.views.mark_as_owned'),
    url(r'^mark_as_read/(?P<apikey>\w+)/(?P<isbn>\w+)/$', 'api.views.mark_as_read'),
)
