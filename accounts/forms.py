from django import forms
from django.forms import *
from django import template
from django.forms.fields import *
from django.forms.widgets import *
from django.forms import ModelForm
from django.template import loader
from django.contrib.auth.models import *


from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import UNUSABLE_PASSWORD, identify_hasher
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site

from django.forms.util import ValidationError
from django.contrib.auth.forms import *
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.db.models.fields.files import *
from django.db.models import *
from .models import *



class UserCreationForm(forms.ModelForm):
    error_messages = {
        'duplicate_username': _("A user with that I.D Number already exists."),
        'password_mismatch': _("PIN must be 4 digits/numbers."),
    }
    id_number = forms.RegexField(
       label=_("Id/Passport Number"), max_length=15,
       regex=r'^[\w.@+-]+$',
        help_text = _("Required. 15 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages = {
            'invalid': _("This value may contain only letters or numbers.")}
    )
    password1 = forms.CharField(
       max_length=50,initial='Choose PIN',
       label=_("Choose PIN"),
       #widget=forms.PasswordInput,
       widget=forms.PasswordInput()
    )
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        

    class Meta:
        model = get_user_model()
        fields = ("full_name","id_number")
      
           
    def clean_id_number(self):
        id_number = self.cleaned_data["id_number"]
        try:
            get_user_model().objects.get(id_number=id_number)
        except get_user_model().DoesNotExist:
            return id_number
        raise forms.ValidationError("A user with that I.DNumber already exists.")
    """
    def clean_id_number(self):
        return clean_unique(self,'id_number')
    """   
    def clean_password1(self):
        password1 = self.cleaned_data.get("password1", "")
        if len(password1) != 4:
            raise forms.ValidationError("PIN must be 4 digits/numbers.")
        return password1
        
    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        
        if len(full_name) > 50:
            raise ValidationError(_('Your name should not exceed 50 characters'))
        return full_name
        
    
          
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
      
                           

        
    
               
class MyAuthForm(forms.Form):
    username = forms.CharField(
    max_length=254,
    label=_('I.D Number')
    )
    password = forms.CharField(
    label=_("Password"), 
    widget=forms.PasswordInput()
    ) 
    
    error_messages = {
        'invalid_login': _("Please enter a correct I.D Number and PIN. "
                           ),
        'no_cookies': _("Your Web browser doesn't appear to have cookies "
                        "enabled. Cookies are required for logging in."),
        'inactive': _("This account is inactive."),
    }
    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        
        self.request = request
        self.user_cache = None
        super(MyAuthForm, self).__init__(*args, **kwargs)
        
       
       

        # Set the label for the "username" field.
        UserModel = get_user_model()
        

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'])
            elif not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages['inactive'])
        self.check_for_test_cookie()
        return self.cleaned_data

    #throws errors:to be deleted
    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(self.error_messages['no_cookies'])

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache



class MyPasswordChangeForm(forms.Form):
    error_messages = {
        'password_mismatch': _("The two PINs  didn't match."),
    }
    old_password = forms.CharField(
       label=_("Current PIN"),
       widget=forms.PasswordInput()
    )
    new_password1 = forms.CharField(
       label=_("New PIN"),
       widget=forms.PasswordInput()
    )
    new_password2 = forms.CharField(
       label=_("Confirm PIN"),
       widget=forms.PasswordInput()
    )
    
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(MyPasswordChangeForm, self).__init__(*args, **kwargs)
   
    def clean_old_password(self):
        UserModel = get_user_model()
        old_password = self.cleaned_data["old_password"]
        self.users_cache = UserModel._default_manager.filter(
        password__iexact=password
        )
        if not len(self.users_cache):
            raise forms.ValidationError(
                self.error_messages['pin_incorrect']
                )
    
        
    def clean_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password')
        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'])
        return new_password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data["new_password1"])
        if commit:
            self.user.save()
        return self.user
        
            

