from __future__ import absolute_import

from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse,resolve
from .models import *
from .views import *


urlpatterns = patterns('business.views',

    url(r'^search/$',SearchView.as_view(),
        name = 'search'),
        
    url(r'^reserve/$',ReservationView.as_view(),
        name='reserve'),
   
    url(r'^successfully_reserved/$',ReservationSuccessView.as_view(),
        name='successfully_reserved'),
     
    url(r'^registration/$',ReservatonCheckView.as_view(),
        name='registration'),
           
    url(r'^register_name/$',RegistrationView.as_view(),
        name = 'register_name'),
        
    url(r'^successfully_registered/$',RegistrationSuccessView.as_view(),
        name='successfully_registered'
    ),
    
    url(r'^faqs/$',FaqsTemplateView.as_view(),
        name ='faqs'
    )
)
