# -*- coding: utf-8 -*-



from django import forms
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.forms.models import inlineformset_factory
from django.forms.formsets import *

from huduma.settings import *
from .models import *

class NameSearchForm(forms.ModelForm):
    class Meta(object):
        model = Searchable
        fields = ('search_term',)
        
    def clean_search_name(self):
        search_term  = self.cleaned_data['search_term ']
        #do_business_here
        try:
           Searchable.objects.get(search_term=search_term)
        except Searchable.DoesNotExist:
             return search_term
        raise forms.ValidationError("That business name already exists")


class ReservationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)  
            if field:
                if type(field.widget) in (forms.TextInput, forms.DateInput):
                    field.widget = forms.TextInput(attrs={'placeholder': field.label})
                    
    class Meta(object):
        model = Reserved
        fields = (
        'name','phone_number',
        'id_number',
        )
        

        
    def clean_name(self):
        name  = self.cleaned_data['name ']
        #do_business_here
        try:
           Reserved.objects.get(name=name)
        except Reserved.DoesNotExist:
             return name
        raise forms.ValidationError("That business name already exists") 
        
    def clean_id_number(self):
        # ajax validation
        pass 
        
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        pass 
        
        
   
        
class ReservationCheckForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ReservationCheckForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)  
            if field:
                if type(field.widget) in (forms.TextInput, forms.DateInput):
                    field.widget = forms.TextInput(attrs={'placeholder': field.label})
                    
    class Meta(object):
        model = Reserved
        fields = (
        'name','phone_number',
        'id_number',
        ) 
        
    def clean_name(self):
        name = self.cleaned_data['name']
        #match_business_name_to_id_number
        pass        
        
class NameRegistrationForm(forms.ModelForm):
   
    def __init__(self, *args, **kwargs):
        super(NameRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['passport_photo'].widget.attrs['class'] = 'fileUpoad'
        self.fields['kra_pin_scan'].widget.attrs['class'] = 'fileUpoad'
        self.fields['id_scan'].widget.attrs['class'] = 'fileUpoad'
        
        for field_name in self.fields:
            field = self.fields.get(field_name)  
            if field:
                if type(field.widget) in (forms.TextInput, forms.DateInput):
                    field.widget = forms.TextInput(attrs={'placeholder': field.label})
                    
    class Meta(object):
        model = Business
        fields = (
        'name','approval_date','business_nature',
        'principal_address','postal_address','id_scan',
        'passport_photo','kra_pin_scan'
        )
        
        
    def clean_id_scan(self): 
        id_scan = self.cleaned_data['id_scan']   
        if 'content-type' in value:  
            main, sub = value['content-type'].split('/')  
            if not (main == 'image' and sub in CONTENT_TYPES):  
                raise forms.ValidationError(u'Please use a JPEG, GIF or PNG image.') 
        else:
            return id_scan 
            
    def clean_passport_photo(self): 
        passport_photo = self.cleaned_data['passport_photo']   
        if 'content-type' in value:  
            main, sub = value['content-type'].split('/')  
            if not (main == 'image' and sub in CONTENT_TYPES):  
                raise forms.ValidationError(u'Please use a JPEG, GIF or PNG image.') 
        else:
            return passport_photo   
            
    def clean_kra_pin_scan(self): 
        kra_pin_scan = self.cleaned_data['kra_pin_scan']   
        if 'content-type' in value:  
            main, sub = value['content-type'].split('/')  
            if not (main == 'image' and sub in CONTENT_TYPES):  
                raise forms.ValidationError(u'Please use a JPEG, GIF or PNG image.') 
        else:
            return kra_pin_scan  
            
            
        
        
RegistrationFormSet = inlineformset_factory(Business,Partners,extra=5)
