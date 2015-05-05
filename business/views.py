import urlparse
from django.shortcuts import *
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth import  *
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from .forms import *
from .models import *
from huduma.settings import *
from ua_detector.views import *
from ua_detector.generic_views import *
from ua_detector.model_views import *



class SearchView(MobileFormView):
    template_name = 'search_form.html'
    mobile_template_name = 'm_search_form.html'
    form_class = NameSearchForm
    success_url = '/business/reserve/'
    
    def form_valid(self, form):
        form.save()
        #return HttpResponseRedirect(self.get_success_url())
        return super(SearchView,self).form_valid(form)
        
    
class ReservationView(CustomCreateView):
    model = Reserved
    form_class = ReservationForm
    template_name ='reservation_form.html'
    mobile_template_name = 'm_reservation_form.html'
    success_url = '/business/successfully_reserved/' 
    
    def form_valid(self, form):
        form.instance.user = self.request.user #Anonymous user 
        return super(ReservationView, self).form_valid(form)
    


class ReservationSuccessView(MobileTemplateView):
    template_name = 'reservation_success.html'
    mobile_template_name = 'm_reservation_success.html' 
    
    
class ReservatonCheckView(MobileFormView):
    template_name = 'check_form.html'
    mobile_template_name = 'm_check_form.html'
    form_class = ReservationCheckForm
    success_url = '/business/register_name/'
    
    def form_valid(self, form):
        return HttpResponseRedirect(self.get_success_url())  
    
"""    
class RegistrationView(CustomCreateView):
    model = Business
    form_class = RegistrationForm
    template_name ='registration_form.html'
    mobile_template_name = 'm_registration_form.html'
    success_url = '/business/successfully_registered/'
    
    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        partners_form = RegistrationFormSet()
        return self.render_to_response(
        self.get_context_data(
        form=form,partners_form=partners_form)
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        partners_form = RegistrationFormSet(self.request.POST)
        
        if (form.is_valid() and partners_form.is_valid()):
            return self.form_valid(form, partners_form)
        else:
            return self.form_invalid(form, partners_form)

    def form_valid(self, form, partners_form):
        self.object = form.save()
        partners_form.instance = self.object
        partners_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, partners_form):
        return self.render_to_response(
        self.get_context_data(
        form=form,partners_form=partners_form)
        )

#see : http://stackoverflow.com/questions/27876644/django-class-based-createview-and-updateview-with-multiple-inline-formsets 
"""

class RegistrationView(MobileFormView):
    form_class = NameRegistrationForm
    template_name ='registration_form.html'
    mobile_template_name = 'm_registration_form.html'
    success_url = '/business/successfully_registered/'
    
    
    def form_valid(self, form):
        form.save()
        return super(RegSuccessView, self).form_valid(form)       
        

class RegistrationSuccessView(MobileTemplateView):
    template_name = 'success.html'  
    mobile_template_name = 'm_success.html'
    
class FaqsTemplateView(MobileTemplateView):
    template_name = 'faqs.html'
    mobile_template_name = 'faqs_mobile.html'
          
