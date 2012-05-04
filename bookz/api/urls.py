from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^import_by_isbn/(?P<isbn>\d+)/$', 'api.views.import_by_isbn'),
)
