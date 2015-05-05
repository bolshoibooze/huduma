from django.contrib import admin
from import_export import resources
from import_export.admin import *
from .models import *

class BusinessResource(resources.ModelResource):
    class Meta(object):
        model = Business
        exclude = ('user','timestamp')
        export_order = (
        'id','name','approval_date','business_nature',
        'principal_address','postal_address','passport_photo',
        'id_scan','kra_pin_scan'
        )
        
class PartnersInline(admin.TabularInline):
    model = Partners
    extra = 30

class BusinessAdmin(admin.ModelAdmin):#ImportExportModelAdmin):
    #prepopulated_fields = {'slug':('name',)}
    fieldsets = (
    ('Details',{
       'fields':(
       'name','approval_date','business_nature',
       'principal_address','postal_address'
       )
    }),
    ('Attachments',{
       'fields':('id_scan','kra_pin_scan')
    })
    )
    list_display = ('name','approval_date')
    resource_class = BusinessResource
    inlines = [PartnersInline]
    list_filter = ('name',)
    exclude = ('user',)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()
    
admin.site.register(Business,BusinessAdmin)


class ReservedResource(resources.ModelResource):
    class Meta(object):
        model = Reserved
        exclude = ('user','created')
        export_order = (
        'id','name','phone_number','id_number',
        'is_reserved','is_confirmed','start_date',
        'end_date'
        )

class ReservedAdmin(admin.ModelAdmin):#ImportExportModelAdmin):
    fieldsets = (
    ('Name',{
       'fields':('name',)
    }),
    ('Reserved By:',{
       'fields':('phone_number','id_number',)
    }),
    ('Status',{
       'fields':(
       'is_reserved','is_confirmed',#'start_date','end_date'
       )
    }),
    
    
    )
    list_display = (
    'name','is_reserved','is_confirmed','start_date',
    'end_date'
    )
    list_filter = ('is_confirmed',)
    exclude = ('user',)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()
        
admin.site.register(Reserved,ReservedAdmin)



class SearchableAdmin(admin.ModelAdmin):
    fieldsets = (
    ('Unavailable Business Names',{
       'fields':('search_term',)
    }),
    )
    list_display = ('search_term',)
    list_filter = ('search_term',)
    
admin.site.register(Searchable,SearchableAdmin)
