from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UserChangeForm
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH
from django.forms import fields
from django.forms import widgets
from django.forms.widgets import NumberInput, Widget
from .models import profile,AddPost,comment
from django.contrib.auth.forms import PasswordChangeForm



''' This is the password change form '''
class passwordchange(PasswordChangeForm):
    old_password=forms.CharField(label_suffix='',widget=forms.TextInput(attrs={'class':'form-control input_user','placeholder':'old password'}))
    new_password1=forms.CharField(label_suffix='',widget=forms.PasswordInput(attrs={'class':'form-control input_user','placeholder':'new password'}))
    new_password2=forms.CharField(label_suffix='',widget=forms.PasswordInput(attrs={'class':'form-control input_user','placeholder':'confirm password'}))
    class Meta:
        model = User

        fields = ['old_password','new_password1','new_password2']


''' This is the comment form for user '''
class commentform(forms.ModelForm):
    content = forms.CharField(label_suffix=' ',label ='',widget = forms.Textarea(attrs={'class':'form-control','rows':2,'placeholder':'comment'}))
    class Meta:
        model  = comment
        fields = ['content']

    
''' These The post form '''
class post(forms.ModelForm):
    title = forms.CharField(label_suffix='',label='Tile',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the title of post'}))
    photo = forms.ImageField(label_suffix='',label='Upload the Pic')
    class Meta:
        model = AddPost
        fields=['title','photo']
        
''' This is the usersign up form which inherits user creation form '''
class usersignform(UserCreationForm):
    username=forms.CharField(label_suffix='',widget=forms.TextInput(attrs={'class':'form-control input_user','placeholder':'Username'}))
    email=forms.EmailField(label_suffix='',widget=forms.EmailInput(attrs={'class':'form-control input_user','placeholder':'Email'}))
    password1= forms.CharField(label_suffix='',widget=forms.PasswordInput(attrs={'class':'form-control input_user','placeholder':'Password'}))
    password2= forms.CharField(label_suffix='',widget=forms.PasswordInput(attrs={'class':'form-control input_user','placeholder':'Confirm Password'}))
    class Meta:
        model = User
        fields = ['username','email']

''' This is the user login form which inhrits authentication form '''
class userloginform(AuthenticationForm):
    username=forms.CharField(label_suffix='',widget=forms.TextInput(attrs={'class':'form-control input_user','placeholder':'Username'}))
    password = forms.CharField(label_suffix='',widget=forms.PasswordInput(attrs={'class':'form-control input_user','placeholder':'Password'}))
    class Meta:
        model = User
        fields=['username']

''' This is the user change form inbuilt form '''
class userchange(UserChangeForm):
    first_name=forms.CharField(label_suffix='',label='First Name ',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name '}))
    last_name=forms.CharField(label_suffix='',label='Last Name',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name '}))
    email=forms.EmailField(label_suffix='',label='Email',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'user@gmail.com '}))
    password=None
    class Meta:
        model = User
        fields =['first_name','last_name','email']

''' These is the profile form which update the user profile '''


class profileform(forms.ModelForm):
    phone=forms.IntegerField(label_suffix='',label='Contact',widget=NumberInput(attrs={'class':'form-control','placeholder':'Mobile NO'}))
    birth_date=forms.DateField(label_suffix='',label='Birth Date',widget=forms.DateInput(attrs={'class':'form-control','placeholder':'YYYY-MM-DD'}))
    photo = forms.ImageField(label_suffix='' ,label='Photo ',)

    class Meta:
        model = profile
        fields = ['phone','birth_date','photo']

