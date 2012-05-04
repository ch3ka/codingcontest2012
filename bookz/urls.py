from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'bookz.views.home', name='home'),
    # url(r'^bookz/', include('bookz.foo.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/' , include('api.urls')),
)
