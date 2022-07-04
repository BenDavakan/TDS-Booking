from django import forms


class ReservationForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(min_length=6, widget=forms.PasswordInput())
    password2 = forms.CharField(min_length=6, widget=forms.PasswordInput())
