from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q
from django.core.mail import send_mail
from django.urls import reverse
from hotels.helpers.availability import check_availability
from hotels.models import Chambre, Hotel, Payement, Ville


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


def search_hotel(request):
    search = request.GET['search']
    date = request.GET['date']
    # date = "Hello word"
    t = date.split("-")
    t1 = t[0]
    t2 = t[1]
    request.session['date01'] = t1
    request.session['date02'] = t2

    ville = Ville.objects.get(name=search)

    room_list = Chambre.objects.filter(hotel__ville=ville)

    # available_rooms = []
    available_hotels = []
    for room in room_list:
        if check_availability(room, t1, t2):
            available_hotels.append(room.hotel)

    # hotels = Hotel.objects.filter(
    #     Q(ville__name=search) | Q(name__icontains=search))
    hotels_number = len(set(available_hotels))
    message = f' {hotels_number} hotels trouvés'

    if hotels_number == 1 or hotels_number == 0:
        message = f'{hotels_number} hotel trouvé'

    # return render(request, 'search_hotel.html', {'hotels': hotels, 'message': message, 'date': date, 't1': t1, 't2': t2})
    return render(request, 'search_hotel.html', {'available_hotels': set(available_hotels), 'message': message, })


def paiement_process(request, number, type):

    transaction_id = request.GET['transaction_id']

    paiement = Payement.objects.create(transaction_id=transaction_id, payment_method=type,
                                       reservation_id=number)

    return HttpResponseRedirect(reverse('home'))
