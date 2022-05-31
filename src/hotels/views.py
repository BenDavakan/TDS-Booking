
from django.shortcuts import get_object_or_404, render

from hotels.models import Chambre, Hotel


def hotels_view(request):
    hotels = Hotel.objects.all()

    return render(request, 'hotels.html', context={"hotels": hotels})


def hotel_detail(request, slug):
    hotel = get_object_or_404(Hotel, slug=slug)

    return render(request, 'detail_hotel.html', context={"hotel": hotel})
