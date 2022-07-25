from django import forms

from accounts.models import CustomUser, Profile
from hotels.models import Reservation


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(min_length=6, widget=forms.PasswordInput())
    password2 = forms.CharField(min_length=6, widget=forms.PasswordInput())


class SigninForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=6, widget=forms.PasswordInput())


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField()
    
