from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30,
                                widget=forms.TextInput(
                                attrs={'placeholder': 'felineconqueror'}))
    f_name = forms.CharField(max_length=50,
                                widget=forms.TextInput(
                                attrs={'placeholder': 'Mr. Feline Jones'}))
    email = forms.EmailField(max_length=50,
                                widget=forms.TextInput(
                                attrs={'placeholder': 'felinejones@gmail.com'}))
    bio = forms.CharField(max_length=100,
                                widget=forms.TextInput(
                                attrs={'placeholder': 'Say something about yourself'}))
