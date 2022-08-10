from curses.ascii import NUL
import decimal
import string
import random
import dateparser

from django.utils.crypto import get_random_string
from django.core.paginator import Paginator
from datetime import date
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from accounts.models import CustomUser
from hotels.models import Chambre, Equipement, Equipement_Hotel, Hotel, Payement, Reservation, Ville

from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


from hotels.helpers.availability import check_availability


def search_hotel(request):

    search = request.GET['search']
    date = request.GET['date']
    t = date.split("-")
    t1 = t[0]
    t2 = t[1]
    price = []

    request.session['date01'] = t1
    request.session['date02'] = t2

    room_list = Chambre.objects.filter(hotel__ville__name=search)

    available_hotels = []
    available_hotels_by_price = []
    for room in room_list:
        if check_availability(room, t1, t2):
            available_hotels.append(room.hotel_id)

    set_hotel = set(available_hotels)

    for item in set_hotel:
        chambres = Chambre.objects.filter(hotel_id=item)
        for chambre in chambres:
            price.append(chambre.overnight)
        available_hotels_by_price.append(
            {'hotel': chambre.hotel, 'price': min(price)})
        price.clear()

    hotels_number = len(set_hotel)
    message = f' {hotels_number} établissements trouvés'

    if hotels_number == 1 or hotels_number == 0:
        message = f'{hotels_number} établissement trouvé'

    return render(request, 'hotels/hotels/search.html', {'available_hotels_by_price': available_hotels_by_price, 'message': message, })


def hotels_view(request):

    hotels = Hotel.objects.all()
    chambres = Chambre.objects.all()
    paginator = Paginator(hotels, 9)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    return render(request, 'hotels/hotels/index.html', context={"hotels": page_object, "chambres": chambres})


def hotel_detail(request, slug):

    hotel = get_object_or_404(Hotel, slug=slug)
    t1 = request.session.get('date01')
    t2 = request.session.get('date02')
    room_list = Chambre.objects.filter(hotel=hotel.id)
    available_rooms = []
    for room in room_list:
        if check_availability(room, t1, t2):
            available_rooms.append(room)

    equipements = Equipement_Hotel.objects.filter(hotel=hotel.id)

    return render(request, 'hotels/hotels/hotel.html', context={"hotel": hotel, "chambres": available_rooms, "equipements": equipements})


def chambre_detail(request, slug, number):

    chambre = get_object_or_404(Chambre, number=number)
    hotel = get_object_or_404(Hotel, slug=slug)
    equipements = Equipement.objects.filter(chambre=chambre.id)

    return render(request, 'detail_chambre.html', context={"chambre": chambre, "hotel": hotel, "equipements": equipements})


def scret_key_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def reservation_hotel(request, slug, number):

    key = scret_key_generator()
    while Reservation.objects.filter(secret_key=key).exists():
        key = scret_key_generator()

    token = get_random_string(length=32)
    while Reservation.objects.filter(token=token).exists():
        token = get_random_string(length=32)

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

            template = render_to_string('hotels/email/new_user.html', {
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
            user_id=user.id, secret_key=key, token=token, chambre_id=chambre.id, check_in=x1, check_out=x2, amount=amount)

        return HttpResponseRedirect(reverse('transition', args=[reserv.id, request.POST.get('check')]))

    return render(request, 'hotels/reservation/index.html', context={"chambre": chambre, "hotel": hotel, "date1": a, "date2": b, "amount": amount, "sejour": sejour, })


def transition(request, number, type):
    reserv = Reservation.objects.get(id=number)
    return render(request, 'hotels/transition.html', {'type_paiement': type, 'reservation': reserv})


def pay_process(request, number, type):

    transaction_id = request.GET['transaction_id']

    token = get_random_string(length=32)
    while Payement.objects.filter(token=token).exists():
        token = get_random_string(length=32)

    Payement.objects.create(transaction_id=transaction_id, token=token, payment_method=type,
                            reservation_id=number)

    reserv = Reservation.objects.get(pk=number)

    template = render_to_string('hotels/email/confirmation_booking.html', {
        'reserv': reserv})

    mail = EmailMessage(
        'TDS Booking | Confiramtion',
        template,
        settings.EMAIL_HOST_USER,
        [reserv.user.email],
    )

    mail.fail_silently = False

    mail.send()

    return redirect('hotels')


def booking_recap(request):
    return render(request, 'hotels/reservation/recap.html')
