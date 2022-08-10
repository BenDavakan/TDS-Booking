
from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect

from django.utils.crypto import get_random_string
from kkiapay import Kkiapay

from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from accounts.forms import CheckBooking, ManagerAddBooking, ManagerEditChambre
from accounts.models import HotelManager
from hotels.models import Chambre, Hotel, Payement, Reservation


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
    return render(request, 'accounts/manager/hotel/index.html', {'hotel': hotel})


def manager_chambres(request):
    user = request.user
    manager = HotelManager.objects.get(user=user.id)

    chambres = Chambre.objects.filter(
        hotel=manager.hotel).exclude(is_delete=True)

    return render(request, 'accounts/manager/chambres/index.html', {'chambres': chambres})


def manager_chambre(request, id):
    chambre = get_object_or_404(Chambre, pk=id)
    if request.method == "POST":
        form = ManagerEditChambre(request.POST, instance=chambre)
        if form.is_valid():
            form.save()
    form = ManagerEditChambre()
    return render(request, 'accounts/manager/chambres/edit.html', {"form": form, 'chambre': chambre})


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

    reservations = Reservation.objects.filter(chambre__hotel=manager.hotel.id)

    return render(request, 'accounts/manager/reservations/index.html', {'reservations': reservations})


def manager_reservation(request, token):
    reservation = get_object_or_404(Reservation, token=token)
    return render(request, 'accounts/manager/reservations/details.html', {'reservation': reservation})


def annul_reservation(request, token):

    reservation = Reservation.objects.get(token=token)
    reservation.status = "AN"
    reservation.save()

    return HttpResponseRedirect(reverse('manager-reservation', args=[token]))


def manager_dashboard(request):
    user = request.user
    manager = HotelManager.objects.get(user=user.id)

    # Count Booking
    booking = Reservation.objects.filter(chambre__hotel=manager.hotel.id)
    total = booking.count()
    booking_cancel = booking.filter(status="AN")
    cancel = booking_cancel.count()
    booking_progress = booking.filter(status="EC")
    progress = booking_progress.count()
    booking_end = booking.filter(status="T")
    end = booking_end.count()

    # Count Payment
    payment = Payement.objects.filter(
        reservation__chambre__hotel=manager.hotel.id)
    total_payment = payment.count()

    # Count Room
    room = Chambre.objects.filter(hotel=manager.hotel.id)
    total_room = room.count()

    return render(request, 'accounts/manager/dashboard/index.html', {'total': total, 'cancel': cancel, 'progress': progress, 'end': end, 'total_payment': total_payment, 'total_room': total_room})


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
    form = ManagerAddBooking()
    return render(request, 'accounts/manager/reservations/add.html', {'form': form})


def delete_room(request, id):
    room = Chambre.objects.get(id=id)
    room.is_delete = True
    room.delete_at = datetime.now()
    room.save()
    return redirect('manager-chambres')


def delete_room_confirm(request, id):
    room = Chambre.objects.get(id=id)
    return render(request, 'accounts/manager/chambres/delete.html', {'room': room})
