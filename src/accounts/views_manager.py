import random
import string
import dateparser
from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect

from django.utils.crypto import get_random_string
from hotels.helpers.availability import check_availability
from hotels.views import scret_key_generator
from kkiapay import Kkiapay
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from accounts.forms import AddChambreImg, AddHotelEp, AddHotelImg, AddPayement, CheckBooking, EditHotel, ManagerAddBooking, ManagerEditChambre
from accounts.models import CustomUser, HotelManager
from hotels.models import Chambre, Equipement, Equipement_Hotel, Hotel, Image_Chambre, Image_Hotel, Payement, Reservation


def add_room(request):
    user = request.user
    manager = HotelManager.objects.get(user=user.id)

    if request.method == "POST":
        form = ManagerEditChambre(request.POST)

        token = get_random_string(length=32)
        while Chambre.objects.filter(token=token).exists():
            token = get_random_string(length=32)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            number = form.cleaned_data.get('number')
            description = form.cleaned_data.get('description')
            area = form.cleaned_data.get('area')
            overnight = form.cleaned_data.get('overnight')
            category = form.cleaned_data.get('category')
            beds = form.cleaned_data.get('beds')
            capacity = form.cleaned_data.get('capacity')

            Chambre.objects.create(hotel=manager.hotel, name=name, number=number, description=description,
                                   area=area, overnight=overnight, beds=beds, category=category, token=token, capacity=capacity)

    form = ManagerEditChambre()

    return render(request, 'accounts/manager/chambres/add.html', {'form': form})


def manager_hotel(request):
    user = request.user
    manager = HotelManager.objects.get(user=user.id)
    hotel = Hotel.objects.get(id=manager.hotel.id)
    eqs = Equipement_Hotel.objects.filter(hotel=manager.hotel)

    if request.method == 'POST':

        Equipement_Hotel.objects.create(
            hotel_id=manager.hotel.id, name=request.POST['name'], number=request.POST['number'], category_id=request.POST['category'])
        return redirect('manager-hotel')
    form = AddHotelEp()

    return render(request, 'accounts/manager/hotel/index.html', {'hotel': hotel, 'form': form, 'eqs': eqs})


def del_hotel_eq(request, id):

    eq = Equipement_Hotel.objects.get(pk=request.POST['equipement'])
    eq.delete()
    return redirect('manager-hotel')


def edit_hotel(request):
    hotel = Hotel.objects.get(pk=request.user.hotelmanager.hotel.id)
    if request.method == 'POST':
        form = EditHotel(request.POST, instance=hotel)

        if form.is_valid():
            form.save()
            return redirect('manager-edit-hotel')
    else:
        form = EditHotel(initial={'description': hotel.description})
    return render(request, 'accounts/manager/hotel/edit_hotel.html', {'form': form, 'hotel': hotel})


def add_hotel_img(request):
    manager = HotelManager.objects.get(user=request.user.id)

    imgs = Image_Hotel.objects.filter(hotel=manager.hotel.id)

    if request.method == 'POST':

        token = get_random_string(length=60)
        while Image_Hotel.objects.filter(token=token).exists():
            token = get_random_string(length=60)

        Image_Hotel.objects.create(
            name=request.POST['name'], token=token, hotel=manager.hotel, image=request.FILES['image'])
        return redirect('add-hotel-img')
    else:
        form = AddHotelImg()

    return render(request, 'accounts/manager/hotel/gallery.html', {'form': form, 'imgs': imgs})


def del_hotel_img(request, token):
    img = Image_Hotel.objects.get(token=token)
    if img.image:
        img.image.delete()
    img.delete()
    return redirect('add-hotel-img')


def manager_chambres(request):
    user = request.user
    manager = HotelManager.objects.get(user=user.id)

    chambres = Chambre.objects.filter(
        hotel=manager.hotel).exclude(is_delete=True)

    return render(request, 'accounts/manager/chambres/index.html', {'chambres': chambres})


def manager_edit_chambre(request, token):
    manager = HotelManager.objects.get(user=request.user.id)
    chambre = get_object_or_404(Chambre, token=token)

    if request.method == "POST":

        Chambre.objects.filter(token=token).update(hotel=manager.hotel.id, description=request.POST['description'], name=request.POST['name'], number=request.POST['number'], overnight=request.POST[
            'overnight'], category=request.POST['category'], beds=request.POST['beds'], capacity=request.POST['capacity'],  area=request.POST['area'], update_at=datetime.now(),)

        return HttpResponseRedirect(reverse('manager-edit-chambre', args=[token]))
    else:

        form = ManagerEditChambre(
            initial={'description': chambre.description, 'category': chambre.category})
    return render(request, 'accounts/manager/chambres/edit.html', {"form": form, 'chambre': chambre})


def manager_chambre_details(request, token):

    room = Chambre.objects.get(token=token)
    equipements = Equipement.objects.filter(chambre=room.id)
    imgs = Image_Chambre.objects.filter(chambre=room.id)

    if request.method == 'POST':

        token = get_random_string(length=60)
        while Image_Chambre.objects.filter(token=token).exists():
            token = get_random_string(length=60)

        Image_Chambre.objects.create(
            name=request.POST['name'], chambre=room, token=token, image=request.FILES['image'])
        return HttpResponseRedirect(reverse('manager-chambre', args=[room.token]))
    else:
        form = AddChambreImg()

    return render(request, 'accounts/manager/chambres/details.html', {'room': room, 'equipements': equipements, 'form': form, 'imgs': imgs})


def del_chambre_img(request, token):
    img = Image_Chambre.objects.get(token=token)
    if img.image:
        img.image.delete()
    img.delete()
    return HttpResponseRedirect(reverse('manager-chambre', args=[img.chambre.token]))


def mes_paiements(request):
    user = request.user
    manager = HotelManager.objects.get(user=user.id)

    paiements = Payement.objects.filter(
        reservation__chambre__hotel=manager.hotel.id)

    return render(request, 'accounts/manager/paiements/index.html', {'paiements': paiements})


def detail_pay(request, token):
    paiement = get_object_or_404(Payement, token=token)

    k = Kkiapay('286874f0fedb11eca56ad905c440058f',
                'tpk_28689c01fedb11eca56ad905c440058f', 'tsk_28689c02fedb11eca56ad905c440058f', sandbox=True)
    transaction = k.verify_transaction(paiement.transaction_id)
    return render(request, 'accounts/manager/paiements/details.html', {'paiement': paiement, 'transaction': transaction, })


def manager_reservations(request):
    user = request.user
    manager = HotelManager.objects.get(user=user.id)

    reservations_EAP = Reservation.objects.filter(
        chambre__hotel=manager.hotel.id, status='EAP')
    reservations_EC = Reservation.objects.filter(
        chambre__hotel=manager.hotel.id, status='EC')
    reservations_AN = Reservation.objects.filter(
        chambre__hotel=manager.hotel.id, status='AN')
    reservations_T = Reservation.objects.filter(
        chambre__hotel=manager.hotel.id, status='T')

    return render(request, 'accounts/manager/reservations/index.html', {'reservations_EAP': reservations_EAP, 'reservations_EC': reservations_EC, 'reservations_AN': reservations_AN, 'reservations_T': reservations_T})


def manager_reservation(request, token):
    reservation = get_object_or_404(Reservation, token=token)
    verify_pay = Payement.objects.filter(reservation=reservation)
    form = AddPayement()
    if request.method == "POST":
        token = get_random_string(length=60)
        while Payement.objects.filter(token=token).exists():
            token = get_random_string(length=60)
        Payement.objects.create(reservation=reservation, token=token,
                                payment_method=request.POST['payment_method'], transaction_id=request.POST['transaction_id'])
    else:
        form = AddPayement()
    return render(request, 'accounts/manager/reservations/details.html', {'reservation': reservation, 'form': form, 'verify_pay': verify_pay})


def annul_reservation(request, token):

    reservation = Reservation.objects.get(token=token)
    reservation.status = "AN"
    reservation.save()

    return HttpResponseRedirect(reverse('manager-reservation', args=[token]))


def manager_dashboard(request):
    user = request.user
    manager = HotelManager.objects.get(user=user.id)

    # Count Booking
    booking = Reservation.objects.filter(
        chambre__hotel=manager.hotel.id)
    total = booking.count()
    booking_cancel = booking.filter(status="AN")
    cancel = booking_cancel.count()
    booking_progress = booking.filter(status="EC")
    progress = booking_progress.count()
    booking_end = booking.filter(status="T")
    end = booking_end.count()
    wait_pay = booking.filter(status="T")
    waiting_pay = wait_pay.count()

    # Count Payment
    payment = Payement.objects.filter(
        reservation__chambre__hotel=manager.hotel.id)
    total_payment = payment.count()

    # Count Room
    room = Chambre.objects.filter(hotel=manager.hotel.id)
    total_room = room.count()

    return render(request, 'accounts/manager/dashboard/index.html', {'total': total, 'cancel': cancel, 'progress': progress, 'waiting_pay': waiting_pay, 'end': end, 'total_payment': total_payment, 'total_room': total_room})


def check_booking(request):
    booking = ""
    msg = ""
    manager = HotelManager.objects.get(user=request.user.id)

    form = CheckBooking(request.GET)

    if form.is_valid():

        code = request.GET['secret_key']

        booking = Reservation.objects.filter(
            chambre__hotel=manager.hotel.id)

        if booking.filter(secret_key=code).exists():

            booking = Reservation.objects.get(secret_key=code)

        else:
            msg = f'{code}'

    form = CheckBooking()

    return render(request, 'accounts/manager/reservations/check.html', {'form': form, 'msg': msg, 'booking': booking})


def add_booking(request):
    user = request.user
    manager = HotelManager.objects.get(user=user.id)
    available_rooms = []
    check_in = ""
    check_out = ""
    form = ManagerAddBooking(request.GET)
    if form.is_valid():

        check_in = str(form.cleaned_data['check_in'])
        check_out = str(form.cleaned_data['check_out'])
        print(type(check_in))

        room_list = Chambre.objects.filter(
            hotel=manager.hotel.id).exclude(is_delete=True)

        for room in room_list:
            if check_availability(room, check_in, check_out):
                available_rooms.append(room)

    return render(request, 'accounts/manager/reservations/add.html', {'form': form, 'available_rooms': available_rooms, 'check_in': check_in, 'check_out': check_out})


def add_booking_form(request, token, check_in, check_out):
    manager = HotelManager.objects.get(user=request.user.id)
    room = Chambre.objects.get(hotel=manager.hotel.id, token=token)
    x1 = dateparser.parse(check_in)
    x2 = dateparser.parse(check_out)
    sejour = (x2 - x1).days
    amount = room.overnight * sejour

    key = scret_key_generator()
    while Reservation.objects.filter(secret_key=key).exists():
        key = scret_key_generator()

    token = get_random_string(length=60)
    while Reservation.objects.filter(token=token).exists():
        token = get_random_string(length=60)

    if request.method == 'POST':

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

        booking = Reservation.objects.create(
            user_id=user.id, secret_key=key, status="EC", token=token, chambre_id=room.id, check_in=x1, check_out=x2, amount=amount)
        return HttpResponseRedirect(reverse('booking-recap', args=[booking.token]))

    return render(request, 'accounts/manager/reservations/add_form.html', {'room': room, 'check_in': x1, 'check_out': x2, 'sejour': sejour, 'amount': amount})


def delete_room(request, token):
    room = Chambre.objects.get(token=token)
    room.is_delete = True
    room.delete_at = datetime.now()
    room.save()
    return redirect('manager-chambres')


def delete_room_confirm(request, token):
    room = Chambre.objects.get(token=token)
    return render(request, 'accounts/manager/chambres/delete.html', {'room': room})


def booking_recap(request, token):
    booking = Reservation.objects.get(token=token)
    if request.method == 'POST':
        tok = get_random_string(length=50)
        while Payement.objects.filter(token=tok).exists():
            tok = get_random_string(length=50)
        Payement.objects.create(
            reservation=booking, payment_method=request.POST['payment_method'], token=token, transaction_id=request.POST['transaction_id'])
        return HttpResponseRedirect(reverse('booking-recap', args=[token]))
    else:
        form = AddPayement()
    return render(request, 'accounts/manager/reservations/recap.html', {'booking': booking, 'form': form})
