from django import forms
from django.db.models import fields
from . models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    username=forms.CharField(help_text=None,label='Username')
    password1=forms.CharField(help_text=None,widget=forms.PasswordInput,label='Password')
    password2=forms.CharField(help_text=None,widget=forms.PasswordInput,label='Confirm Password')
    class Meta:
        model=User
        fields=('username','password1','password2')
        labels=('password1','password','password2','confirm password')

class ProfileForm(forms.ModelForm):
    address=forms.Textarea()
    customer='customer'
    staff='staff'
    user_types=[
        (customer,'customer'),
        (staff,'staff')
    ]
    user_type=forms.ChoiceField(required=True,choices=user_types)
    class Meta:
        model=Register
        fields=('address','phone','user_type')

class UpdateForm(forms.ModelForm):
    username=forms.CharField(help_text=None,label='Username')
    firstname=forms.CharField(help_text=None,label='firstname')
    lastname=forms.CharField(help_text=None,label='lastname')
    class Meta:
        model=User
        fields=('username','firstname','lastname')

class UpdateProfileForm(forms.ModelForm):
    address=forms.Textarea()
    
    class Meta:
        model=Register
        fields=('address','phone')

class ComplaintForm(forms.ModelForm):
    content=forms.Textarea()
    class Meta:
        model=Complaints
        fields=('content','reason')


class FeedbackForm(forms.ModelForm):
    content=forms.Textarea()
    class Meta:
        model=Feedback
        fields=('content',)


class RequirementForm(forms.ModelForm):
    description=forms.Textarea()
    class Meta:
        model=Requiremt
        fields=('description','square_feet')

class UpdateRequirementForm(forms.ModelForm):
    description=forms.Textarea()
    class Meta:
        model=Requiremt
        fields=('description','status','demo','message','work','percentage')


class ChatForm(forms.ModelForm):
    content=forms.Textarea()
    class Meta:
        model=Chat
        fields=('content',)

    
class LeaveForm(forms.ModelForm):
    startdate=forms.DateField()
    class Meta:
        model=Leave
        fields=('startdate','days','reason')


