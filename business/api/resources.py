import datetime
from business.models import *
from tastypie.resources import *
from tastypie.authorization import DjangoAuthorization
from tastypie.serializers import Serializer
from tastypie.authentication import *

       
class BusinessResource(ModelResource):
    class Meta:
        resource_name = 'business'
        queryset = Business.objects.all()
        allowed_methods = ['get','post','patch','get']
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        list_allowed_methods = ['get','post','patch']
        detail_allowed_methods = ['get','post','patch']
        fields = [
        'name','approval_date','business_nature',
        'principal_address','postal_address','user'
        ]
        
    def apply_authorization_limits(self, request, object_list):
    	    return object_list.filter(user=request.user)
    	    
    def obj_create(self, bundle, **kwargs):
        return super(BusinessResource, self).obj_create(
        bundle, user=bundle.request.user
        )
        
    def obj_update(self, bundle, **kwargs): 
        return super(BusinessResource,self).obj_update(
        bundle,user=bundle.request.user
        )        
    
    
    
    
    
    
class ReservedResource(ModelResource):
    class Meta(object):
        resource_name = 'reserved'
        queryset = Reserved.objects.all()
        serializer = Serializer(formats=['json',])
        authorization= DjangoAuthorization()
        authentication = ApiKeyAuthentication()
        list_allowed_methods = ['get','post','patch']
        detail_allowed_methods = ['get','post','patch']
    	fields = [
    	'name','phone_number','id_number',
        'is_reserved','is_confirmed','start_date',
        'end_date','user'
    	]
    	
    def obj_create(self, bundle, **kwargs):
        return super(ReservedResource, self).obj_create(
        bundle, user=bundle.request.user
        )

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)
        
    def obj_update(self, bundle, **kwargs): 
        return super(ReservedResource,self).obj_update(
        bundle,user=bundle.request.user
        )        
