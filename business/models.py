import logging
import datetime
from django.db import models
from django.db.models import *
from django.conf import settings
from django.utils import timezone

from django.utils.text import *
from django.db.models.query import *
from django.contrib.auth.models import *
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from django.utils.encoding import smart_unicode
from django.db.models import get_model
from huduma.settings import *

# All models should allow for import/export of data in 
# popular formats like excel et al.

# Writing a letter requesting for search is unecessary
# since it's only used for doing the actual search


        
# user logs in with the MM number &
# is assigned the no. of searches to do

"""
***  might be used in lieu of tasks  ***
def reservations_wrapper(sender,**kwargs):
    from ua_detector.models import reservation
    reservations(sender,**kwargs)
    
def registered_wrapper(sender,**kwargs):
    from ua_detector.models import registered
    registered(sender,**kwargs)
"""


class Business(models.Model):
    name = models.CharField(
       max_length=50,db_index=True,
       verbose_name='Business Name',
       help_text = 'must have enterprises,\
       ventures,tours & travel:create list \
       of allowed terms'
    )
    approval_date = models.DateField(
       auto_now_add=False,
       verbose_name = 'Approval Date'
    )
    business_nature = models.TextField(
       max_length= 280,
       verbose_name='Nature of Business'
    )
    principal_address = models.TextField(
       max_length=140,help_text='Plot No.\
       ,Section & Name of The Street/Road',
       verbose_name='Principal Address'
    )
    postal_address = models.TextField(
       max_length=140,
       verbose_name='Postal Address'
    )
    #if these details are used by other
    # GoK services,create a separate auth app 
    passport_photo = models.ImageField(
       upload_to='people/passport_photo',
       verbose_name='Passport Photo Scan'
    )
    id_scan = models.ImageField(
       upload_to='people/id_scans',
       verbose_name='I.D Scan'
    )
    kra_pin_scan = models.ImageField(
       upload_to='people/kra_scans',
       verbose_name='KRA  Scan'
    )
    slug = models.SlugField(
       max_length=100
    )
    timestamp = models.DateTimeField(
       auto_now_add=True
    )
    user = models.ForeignKey(
       settings.AUTH_USER_MODEL, 
       related_name='+',null=True,
       blank=True,help_text='admin'
    )
    class Meta(object):
        db_table = 'Business'
        verbose_name_plural='Businesses'
        
    def __unicode__(self):
        return self.name 
        
    def save(self,*args,**kwargs):
        if not self.id:
           self.slug = slugify(self.name)
        super(Business,self).save(*args,**kwargs)
 
#might be used in lie of tasks later on        
#models.signals.post_save.connect(reservations_wrapper,sender=Business) 


  
class Partners(models.Model):
    business = models.ForeignKey(
      Business,related_name='+'
    )
    full_name = models.CharField(
      max_length=50,
      verbose_name='First& Last name'
    )
    nationality = models.CharField(
      max_length=50,
      help_text='Choice Field',
      verbose_name='Nationality'
    )
    origin = models.CharField(
      max_length=50,
      verbose_name='Nationality of Origin'
    )
    age = models.IntegerField(
      verbose_name='Age'
    )
    sex = models.CharField(
      max_length=100,default=2,
      choices = settings.GENDER,
      verbose_name='Gender'
    )
    other = models.TextField(
      max_length=140,
      verbose_name='Other Business/Occupation'
    )
    class Meta(object):
        db_table='Partner' 
        verbose_name_plural='Partners'
      
    def __unicode__(self):
        return self.full_name
        
    def save(self,*args,**kwargs):
        super(Partner,self).save(*args,**kwargs)
      
      


class Reserved(models.Model):
    name = models.CharField(
       max_length=50,help_text='You can\
        only confirm one name at a time',
        verbose_name='Business Name'
    )
    phone_number = models.CharField(
       max_length=12,
       verbose_name='Your Phone Number '
    )
    id_number = models.CharField(
       max_length=10,
       verbose_name='Your I.D Number'
    )
    is_reserved = models.BooleanField(
       default=False
    )
    is_confirmed = models.BooleanField(
       default=False
    )
    start_date = models.DateField(
       auto_now_add=True,
       verbose_name='Confirmation Date'
    ) 
    end_date = models.DateField(
       auto_now_add=False,
       verbose_name='Expiration Date'
    )
    user = models.ForeignKey(
       settings.AUTH_USER_MODEL, 
       related_name='+',null=True,
       blank=True,help_text='admin'
    )
    created = models.DateTimeField(
       auto_now_add=True
    ) 
    class Meta(object):
        db_table ='Reserved'
        verbose_name_plural='Reserved'
        
    def __unicode__(self):
        return unicode(self.business) 
  
               
    def save(self,*args,**kwargs):
        #update is_reserved=True
        if self.end_date is None:
           end_date = self.start_date + datetime.timedelta(days=30)
           self.end_date = end_date
           self.save()
        super(Reserved,self).save(*args,**kwargs)  

#models.signals.post_save.connect(reservations_wrapper,sender=Reserved)         
        
class Searchable(models.Model):
    search_term = models.CharField(
       max_length=50,db_index=True,
       verbose_name='Business Name'
    )
    timestamp = models.DateTimeField(
       auto_now_add=True
    )  
    class Meta(object):
        db_table ='Searchable'
        verbose_name_plural = 'Searchable'
        
    def __unicode__(self):
        return self.search_term
        
    def save(self,*args,**kwargs):
        super(Searchable,self).save(*args,**kwargs)
        
               
