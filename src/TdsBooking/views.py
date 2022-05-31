from django.shortcuts import render


def home_view(request):
    return render(request, 'accueil.html', context={"prenom": "M. DAVAKAN"})


def contact_view(request):
    return render(request, 'contact.html')
