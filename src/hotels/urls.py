from django.urls import path
from hotels.views import chambre_detail, hotel_detail, hotels_view, reservation_hotel

urlpatterns = [
    path('', hotels_view, name="hotels-index"),
    path('<str:slug>/', hotel_detail, name='hotel'),
    path('<str:slug>/chambre-<int:number>/',
         chambre_detail, name='chambre'),
    path('<str:slug>/chambre-<int:number>/reservation/',
         reservation_hotel, name='reservation'),

]
