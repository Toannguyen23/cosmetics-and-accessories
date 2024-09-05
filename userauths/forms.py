from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'email'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'password'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'repeat password'}))
    
    class Meta:
        model = User
        fields = ['username','email']