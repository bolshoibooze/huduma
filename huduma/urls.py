from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from yawdadmin import admin_site
admin_site._registry.update(admin.site._registry)

from tastypie.api import Api
from business.api.resources import *


v1_api = Api(api_name='v1')
v1_api.register(BusinessResource())
v1_api.register(ReservedResource())


urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls)),
    url(r'^business/', include('business.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
