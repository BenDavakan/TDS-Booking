from django.shortcuts import render
from django.db.models import Q

from hotels.models import Hotel


def home_view(request):
    hotels = Hotel.objects.all()[:5]

    return render(request, 'accueil.html', {"hotels": hotels})


def contact_view(request):
    return render(request, 'contact.html')


def a_propos_view(request):
    return render(request, 'a_propos.html')


def search_hotel(request):
    search = request.GET['search']
    date = request.GET['date']
    # date = "Hello word"
    t = date.split("-")
    t1 = t[0]
    t2 = t[1]
    request.session['date1'] = t1
    request.session['date2'] = t2

    hotels = Hotel.objects.filter(
        Q(ville__iexact=search) | Q(name__icontains=search))
    hotels_number = hotels.count()
    message = f' {hotels_number} hotels trouvés'

    if hotels_number == 1 or hotels_number == 0:
        message = f'{hotels_number} hotel trouvé'

    return render(request, 'search_hotel.html', {'hotels': hotels, 'message': message, 'date': date, 't1': t1, 't2': t2})
