from pyexpat import model
from attr import fields
from django import forms

from accounts.models import CustomUser, Profile
from hotels.models import Chambre, Equipement_Hotel, Hotel, Image_Chambre, Image_Hotel, Payement


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(min_length=6, widget=forms.PasswordInput())
    password2 = forms.CharField(min_length=6, widget=forms.PasswordInput())


class SigninForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=6, widget=forms.PasswordInput())


class AddHotelImg(forms.ModelForm):
    class Meta:
        model = Image_Hotel
        fields = [
            'name',
            'image',
            
        ]
class EditHotel(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = [
            'name',
            'description',
            'tel_1',
            'tel_2',
            'email',
            'adress',
            'ville',
            'star_nbr',  
        ]
class AddHotelEp(forms.ModelForm):
    class Meta:
        model=Equipement_Hotel
        fields = [
            'name',
            'number',
            'category',
        ]


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
            'profile_pic',
            'update_at',
        ]

        Widgets = {'birthdate': forms.SelectDateWidget(
            years=range(1990, 2025))}


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
            'capacity',
        ]
class AddChambreImg(forms.ModelForm):
    class Meta:
        model = Image_Chambre
        fields = [
            'name',
            'image',  
        ]


class CheckBooking(forms.Form):
    secret_key = forms.CharField(min_length=6, required=True)


class DateInput(forms.DateInput):
    input_type = 'date'


class ManagerAddBooking(forms.Form):
    check_in = forms.DateField()
    check_out = forms.DateField()
    
class AddPayement(forms.ModelForm):
    class Meta:
        model = Payement
        fields = [
            'payment_method',
            'transaction_id',
           
        ]
        
