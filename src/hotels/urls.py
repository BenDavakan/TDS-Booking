from django.urls import path
from hotels.views import chambre_detail, hotel_detail, hotels_view, pay_process, reservation_hotel, search_hotel

urlpatterns = [
    path('', hotels_view, name="hotels-index"),
    path('<str:slug>/', hotel_detail, name='hotel'),
    path('<str:slug>/chambre-<int:number>/',
         chambre_detail, name='chambre'),
    path('<str:slug>/chambre-<int:number>/reservation/',
         reservation_hotel, name='reservation'),
    path('reservation', search_hotel, name='name_search_hotel'),
    path('paiement/<int:number>/<str:type>/paiement-process/',
         pay_process, name='paiement_process'),

    path('reservation/recap/',
         pay_process, name='recap'),

]
