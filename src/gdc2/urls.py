from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import visualize


urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'visualize.views.index'),
    url(r'^status/$', 'visualize.views.status'),
    url(r'^language/(?P<lang>[a-zA-Z0-9_\-\+\#]+).json$', 'visualize.views.language'),
)