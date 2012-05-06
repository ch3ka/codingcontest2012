from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import login, logout

from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.models import User, Group
#admin.site.unregister(User)
#admin.site.unregister(Group)

urlpatterns = patterns('',
    # url(r'^$', 'bookz.views.home', name='home'),
    # url(r'^bookz/', include('bookz.foo.urls')),
    url(r'^$', 'book.views.index'),
    url(r'^about/$', 'book.views.about'),
    url(r'^books/$', 'book.views.books'),
    url(r'^books/(?P<by>\w+)/(?P<key>.*)/$', 'book.views.books_by'),
    url(r'^authors/$', 'book.views.authors'),
    url(r'^publishers/$', 'book.views.publishers'),
    url(r'^subjects/$', 'book.views.subjects'),
    url(r'^book/(?P<isbn>\d+)/$', 'book.views.book'),
    url(r'^book/new/$', 'book.views.addbook'),
    url(r'^book/edit/(?P<isbn>\d+)/$', 'book.views.editbook'),
    url(r'^book/read/(?P<isbn>\d+)/$', 'book.views.readbook'),
    url(r'^book/own/(?P<isbn>\d+)/$', 'book.views.ownbook'),
    url(r'^book/review/(?P<isbn>\d+)/$', 'book.views.reviewbook'),
    url(r'^comment/(?P<reviewid>\d+)/$', 'book.views.comment'),
    url(r'^author/(?P<author_id>.*)/$', 'book.views.author'),
    url(r'^publisher/(?P<publisher_id>\w+)/$', 'book.views.publisher'),
    url(r'^subject/(?P<subject_id>.*)/$', 'book.views.subject'),
    url(r'^login/$',  login),
    url(r'^logout/$', logout, {'template_name': 'registration/loggedout.html'}),
    url(r'^accounts/login/$',  login),
    url(r'^accounts/logout/$', logout, {'template_name': 'registration/loggedout.html'}),
    url(r'^accounts/profile/$', 'accounts.views.own_profile'),
    url(r'^accounts/profiles/(?P<user>\w+)/$', 'accounts.views.profile'),
    url(r'^loggedin/$', direct_to_template, {'template': 'registration/loggedin.html'}),
    url(r'^register/$', 'accounts.views.register'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/' , include('api.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)

urlpatterns += staticfiles_urlpatterns()
