from pyexpat import model
from django import forms
from django.forms import ModelForm

from accounts.models import CustomUser, Profile
from hotels.models import Chambre, Reservation


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


class ManagerEditChambre(ModelForm):
    class Meta:
        model = Chambre
        fields = [
            'number',
            'name',
            'description',
            'overnight',
            'area',
            'beds',
            'category',
        ]
