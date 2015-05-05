from __future__ import absolute_import


import datetime
from django.db import *
from celery import Celery
from celery import shared_task
from django.conf import settings
from celery.utils.log import get_task_logger
from django.utils.translation import ugettext as _
from socket import error as socket_error
from celery.contrib.methods import *
from django.utils import timezone
from django.db.models import *


from business.models import *
# since querysets are lazy .....
reserved = Reserved.objects.all()
names = Business.objects.all()
today = datetime.date.today()
searchable = Searchable.objects.all()

@shared_task()
def unlock_unconfirmed_names():
    for obj in reserved.filter(Q(is_confirmed=False)& Q(end_date=today)).iterator():
        return reserved.select_for_update().update(is_reserved=False)
        #run this every 24 hrs
        
        
@shared_task()       
def confirmed_name():
    for obj in names.filter(timestamp__lte=today).iterator():
        for u in reserved.filter(Q(is_confirmed=False)& Q(is_reserved=True)).iterator():
            return reserved.select_for_update().filter(business_name__exact=obj.name).update(
            is_confirmed=True
            )
               
@shared_task()               
def update_reserved_names():
    for obj in reserved.filter(is_reserved=True).iterator():
        name_search = searchable.filter(search_term__exact=obj.name)
        if name_search.exists():
           pass 
        else:
            return search.select_for_update().update(search_term=obj.name)
            
            
            
            
@shared_task()               
def update_registered_names():
    for obj in business.iterator():#limit this to only the name 
        name_search = searchable.filter(search_term__exact=obj.name)
        if name_search.exists():
           pass 
        else:
            return search.select_for_update().update(search_term=obj.name)
            
            

