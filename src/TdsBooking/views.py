
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.db.models import Q
from django.core.mail import send_mail
from django.urls import reverse
from hotels.helpers.availability import check_availability
from hotels.models import Chambre, Hotel, Payement, Reservation
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string


def home_view(request):
    hotels = Hotel.objects.all()[:5]

    return render(request, 'accueil.html', {"hotels": hotels})


def contact_view(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')

        send_mail(
            subject,
            message,
            email,
            ['bdkmailpro@gmail.com'],
            fail_silently=False,
        )

    return render(request, 'contact.html', {})


def a_propos_view(request):
    return render(request, 'a_propos.html')
