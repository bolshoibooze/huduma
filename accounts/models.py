from __future__ import(
absolute_import, unicode_literals
) 

from django.db import models
from django.db.models import *
from django.contrib import auth
from django.dispatch import receiver
from django.db.models.signals import *
from django.contrib.auth.models import *
from django.contrib.auth.signals import user_logged_in

from django.db.models.manager import EmptyManager
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, id_number, password=None, **extra_fields):
        now = timezone.now()
        if not id_number:
            raise ValueError('The given I.D number must be set')
        #email = UserManager.normalize_email(email)
        user = self.model(id_number=id_number,
                          is_staff=False,is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)
 
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, id_number, password, **extra_fields):
        u = self.create_user(id_number, password, **extra_fields)
        u.is_admin = True
        u.save(using=self._db)
        return u
    


class CustomUser(AbstractBaseUser):
    full_name = models.CharField(
       max_length=50,
       verbose_name='Full Name',
       help_text='First & Last name'
    )
    id_number = models.IntegerField(
       verbose_name='I.D Number',
       unique=True,db_index=True
    )
    mug_shot = models.ImageField(
       upload_to='staff/passport_photos',
       verbose_name='Staff Photo',
       null=True,blank=True,
    )
    is_staff = models.BooleanField(
       default=False
    )
    is_superuser = models.BooleanField(
       default=False
    )
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    login_attempts = models.IntegerField(
       default=0,null=True,blank=True
    )
    USERNAME_FIELD = 'id_number'
    REQUIRED_FIELDS = ['full_name',]
    objects = CustomUserManager()
    class Meta(object):
        db_table = 'CustomUser'
        verbose_name_plural = 'CustomUsers'
        
    def __unicode__(self):
        return self.full_name
    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.full_name)
           
    def get_full_name(self):
        #the user is identified by their id_number
        return self.full_name
        
    def get_short_name(self):
        return self.full_name
        
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
        
    def save(self,*args,**kwargs):
        super(CustomUser,self).save(*args,**kwargs)
