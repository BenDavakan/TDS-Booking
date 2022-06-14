from django.shortcuts import render

from TdsBooking.forms import SignupForm, SigninForm

def home_view(request):
    return render(request, 'accueil.html')


def contact_view(request):
    return render(request, 'contact.html')


def connexion_view(request):
    form = SigninForm()
    return render(request, 'signin.html', {"form": form})


def inscription_view(request):
    form = SignupForm()
    return render(request, 'signup.html', {"form": form})


def a_propos_view(request):
    return render(request, 'a_propos.html')
