from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from kkiapay import Kkiapay


from django.shortcuts import render

from django.urls import reverse

from hotels.models import Payement, Reservation


def mes_reservations(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user.id)

    return render(request, 'accounts/customer/reservations/index.html', {'reservations': reservations})


def detail_reservation(request, token):

    reservation = get_object_or_404(Reservation, token=token)

    return render(request, 'accounts/customer/reservations/details.html', {'reservation': reservation})


def annul_reservation(request, token):

    reservation = Reservation.objects.get(token=token)
    reservation.status = "AN"
    reservation.save()

    return HttpResponseRedirect(reverse('reservation', args=[token]))


def mes_paiements(request):
    user = request.user

    paiements = Payement.objects.filter(reservation__user=user)

    return render(request, 'accounts/customer/paiements/index.html', {'paiements': paiements})


def detail_paiement(request, token):
    paiement = get_object_or_404(Payement, token=token)

    k = Kkiapay('286874f0fedb11eca56ad905c440058f',
                'tpk_28689c01fedb11eca56ad905c440058f', 'tsk_28689c02fedb11eca56ad905c440058f', sandbox=True)
    transaction = k.verify_transaction(paiement.transaction_id)
    return render(request, 'accounts/customer/paiements/details.html', {'paiement': paiement, 'transaction': transaction, })


def customer_dashboard(request):

    booking = Reservation.objects.filter(user=request.user.id)
    total = booking.count()
    booking_cancel = booking.filter(status="AN")
    cancel = booking_cancel.count()
    booking_progress = booking.filter(status="EC")
    progress = booking_progress.count()
    booking_end = booking.filter(status="T")
    end = booking_end.count()

    payment = Payement.objects.filter(reservation__user=request.user.id)
    total_payment = payment.count()

    return render(request, 'accounts/customer/dashboard/index.html', {'total': total, 'total_payment': total_payment})
