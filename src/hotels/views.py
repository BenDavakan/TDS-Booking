import string
import random
from django.core.paginator import Paginator
from datetime import date
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import CustomUser, MyUserManager
from hotels.models import Chambre, Equipement, Hotel, Reservation


from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from pprint import pprint


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

    return render(request, 'detail_hotel.html', context={"hotel": hotel, "chambres": chambres})


def chambre_detail(request, slug, number):

    chambre = get_object_or_404(Chambre, number=number)
    hotel = get_object_or_404(Hotel, slug=slug)
    equipements = Equipement.objects.filter(chambre=chambre.id)

    return render(request, 'detail_chambre.html', context={"chambre": chambre, "hotel": hotel, "equipements": equipements})


def reservation_hotel(request, slug, number):
    chambre = Chambre.objects.get(number=number)
    hotel = Hotel.objects.get(slug=slug)

    if request.method == "POST":
        date1 = request.session.get('date1')
        date2 = request.session.get('date2')
        datea = date(2022, 10, 1)
        dateb = date(2022, 10, 11)
        date0 = dateb - datea
        print(date0.days)
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        if request.user.is_authenticated:
            user = request.user

        else:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            tel = request.POST.get('tel')
            password = ''
            characters = list(string.ascii_letters +
                              string.digits + "!@#$%&()")
            for i in range(8):
                password += random.choice(characters)
            print(password)
            if CustomUser.objects.filter(email=email).exists():
                messages.info(
                    request, "L'email est déja pris!! Réessayez avez un autre.")
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

        Reservation.objects.create(
            user_id=user.id, chambre_id=chambre.id, check_in='2022-10-22', check_out='2022-10-27')

    return render(request, 'reservation_hotel.html', context={"chambre": chambre, "hotel": hotel})
