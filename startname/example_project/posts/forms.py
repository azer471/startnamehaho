from django.forms import ModelForm, Textarea
from django.utils.translation import ugettext_lazy as _
from .models import Article
from django import forms

from django.core.validators import RegexValidator
#para Form User
from django.contrib.auth.models import User
from django.utils import timezone

class ArticleCreate(forms.ModelForm):
    alphanumeric = RegexValidator(r'^[\u0621-\u064A0-9a-zA-Z ]*$', 'في ’عنوان الخبر‘ يرجى استخدام حروف فقط (من الألف إلى الياء) والأرقام')
    class Meta:
        model = Article
        fields = ('title','description','pageweb','url')



        labels = {
            'title': _('عنوان الخبر'),
            'description': _('تفاصيل الخبر'),           
            'pageweb': _('أسم الموقع الألكترونى'),
            'url': _('الرابط'),
        }

#        help_texts = {
#            'title': _('Some useful help text.'),
#        }
        error_messages = {
            'title': {
                'max_length': _("المرجو الانتباه أثناء الكتابة، لقد تم تجاوز الحد المسموح به"),
                'required': _("يرجى ملء المعلومة التالية"),
            },
            'description': {
                'max_length': _("المرجو الانتباه أثناء الكتابة، لقد تم تجاوز الحد المسموح به"),
                'required': _("يرجى ملء المعلومة التالية"),
            },

            'pageweb': {
                'max_length': _("المرجو الانتباه أثناء الكتابة، لقد تم تجاوز الحد المسموح به"),
                'required': _("يرجى ملء المعلومة التالية"),
            },
            'url': {
                'max_length': _("المرجو الانتباه أثناء الكتابة، لقد تم تجاوز الحد المسموح به"),
                'required': _("يرجى ملء المعلومة التالية"),
            },            
        }



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label= 'كلمة السر', error_messages = {'required': _("يرجى ملء المعلومة التالية")})
                
    confirm_password = forms.CharField(widget=forms.PasswordInput, label= 'اعد كلمة السر', error_messages = {'required': _("يرجى ملء المعلومة التالية")})
    
    class Meta:
        model = User
        fields = ('username','email','password')


        labels = {
            'username': _('المستخدم'),        
            'email': _('البريد الإلكتروني'),
        }
        error_messages = {
            'username': {
                'required': _("يرجى ملء المعلومة التالية"),
            },
            'email': {
                'required': _("يرجى ملء المعلومة التالية"),
            },

            'password': {
                'required': _("يرجى ملء المعلومة التالية"),
            },
          
        }


    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', 'كلمة السر غير متطابقة.')

    def save(self, commit=True):
        user = super(UserForm, self).save(commit)
        user.last_login = timezone.now()
        if commit:
            user.save()        
        return user