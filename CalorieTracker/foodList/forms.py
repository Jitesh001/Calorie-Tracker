from pyexpat import model
from django import forms
from django.contrib.auth.models import User #imported User model
from django.contrib.auth.forms import UserCreationForm #usercreation form

class RegisterForm(UserCreationForm):   #inherited built in usercreationform
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
