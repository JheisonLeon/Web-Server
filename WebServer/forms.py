from django.forms import ModelForm
from django import forms
from .models import Usuario

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Usuario
        fields=[
           'username',
           'password'
            ]
        widgets = {
            'password': forms.PasswordInput()
         }
