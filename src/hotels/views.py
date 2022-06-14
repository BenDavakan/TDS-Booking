
from django.core.paginator import Paginator

from django.shortcuts import get_object_or_404, render

from hotels.models import Chambre, Hotel, Category



def hotels_view(request):
    hotels = Hotel.objects.all()
    chambres= Chambre.objects.all()
    paginator = Paginator(hotels, 9)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    return render(request, 'hotels.html', context={"hotels": page_object, "chambres": chambres})


def hotel_detail(request, slug):
    hotel = get_object_or_404(Hotel, slug=slug)
    
    # chambres = Chambre.objects.filter(hotel=hotel.id)
    chambres = Chambre.objects.filter(hotel=hotel.id)
    

    return render(request, 'detail_hotel.html', context={"hotel": hotel, "chambres" : chambres})

def chambre_detail(request, number):
    
    chambre = get_object_or_404(Chambre, number=number)
    
    return render(request, 'detail_chambre.html', context={"chambre": chambre})