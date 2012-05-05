from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.models import User, Group
admin.site.unregister(User)
admin.site.unregister(Group)

urlpatterns = patterns('',
    # url(r'^$', 'bookz.views.home', name='home'),
    # url(r'^bookz/', include('bookz.foo.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/' , include('api.urls')),
)

urlpatterns += staticfiles_urlpatterns()
