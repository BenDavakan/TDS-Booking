import decimal
import string
import random
import dateparser
from django.core.paginator import Paginator
from datetime import date
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from accounts.models import CustomUser, MyUserManager
from hotels.models import Chambre, Equipement, Equipement_Hotel, Hotel, Reservation, Ville

import datetime

from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from pprint import pprint


def villes_view(request):
    villes = Ville.objects.all()

    x = Hotel.objects.filter(ville__name='Parakou').count()

    return render(request, 'villes.html', {'villes': villes, 'x': x})


def hotels_view(request):
    hotels = Hotel.objects.all()
    chambres = Chambre.objects.all()
    paginator = Paginator(hotels, 9)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    return render(request, 'hotels.html', context={"hotels": page_object, "chambres": chambres})


def hotel_detail(request, slug):
    hotel = get_object_or_404(Hotel, slug=slug)

    # chambres = Chambre.objects.filter(hotel=hotel.id)
    chambres = Chambre.objects.filter(hotel=hotel.id)
    equipements = Equipement_Hotel.objects.filter(hotel=hotel.id)

    return render(request, 'detail_hotel.html', context={"hotel": hotel, "chambres": chambres, "equipements": equipements})


def chambre_detail(request, slug, number):

    chambre = get_object_or_404(Chambre, number=number)
    hotel = get_object_or_404(Hotel, slug=slug)
    equipements = Equipement.objects.filter(chambre=chambre.id)

    return render(request, 'detail_chambre.html', context={"chambre": chambre, "hotel": hotel, "equipements": equipements})


def reservation_hotel(request, slug, number):
    chambre = Chambre.objects.get(number=number)
    hotel = Hotel.objects.get(slug=slug)
    a = request.session.get('date01')
    b = request.session.get('date02')
    mode = request.POST.get('check')
    x1 = dateparser.parse(a)
    x2 = dateparser.parse(b)
    sejour = (x2 - x1).days
    amount = chambre.overnight * sejour
    user = ""
    if request.method == "POST":

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        tel = request.POST.get('tel')
        password = ''
        characters = list(string.ascii_letters + string.digits + "!@#$%&()")
        for i in range(8):
            password += random.choice(characters)
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)

        else:
            user = CustomUser.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, password=password, tel=tel,)
            template = render_to_string('email_template.html', {
                'first_name': first_name, 'last_name': last_name, 'password': password, 'email': email})
            mail = EmailMessage(
                'TDS Booking',
                template,
                settings.EMAIL_HOST_USER,
                [email],
            )
            mail.fail_silently = False
            mail.send()

        reserv = Reservation.objects.create(
            user_id=user.id, chambre_id=chambre.id, check_in=x1, check_out=x2, amount=amount)

        return HttpResponseRedirect(reverse('transition', args=[reserv.id, request.POST.get('check')]))

    return render(request, 'reservation_hotel.html', context={"chambre": chambre, "hotel": hotel, "date1": a, "date2": b, "amount": amount, "sejour": sejour, })


def transition(request, number, type):
    reserv = Reservation.objects.get(id=number)
    return render(request, 'transition.html', {'type_paiement': type, 'reservation': reserv})
