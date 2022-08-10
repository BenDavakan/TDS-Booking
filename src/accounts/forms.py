from pyexpat import model
from attr import fields
from django import forms

from accounts.models import CustomUser, Profile
from hotels.models import Chambre


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(min_length=6, widget=forms.PasswordInput())
    password2 = forms.CharField(min_length=6, widget=forms.PasswordInput())


class SigninForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=6, widget=forms.PasswordInput())


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'tel',
        ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'gender',
            'birthdate',
            'country',
        ]


class ManagerEditChambre(forms.ModelForm):
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
            'capacity'
        ]


class CheckBooking(forms.Form):
    secret_key = forms.CharField(min_length=6, required=True)


class DateInput(forms.DateInput):
    input_type = 'date'


class ManagerAddBooking(forms.Form):
    check_in = forms.DateField(widget=DateInput)
    check_out = forms.DateField()
