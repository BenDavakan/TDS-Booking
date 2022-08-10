from django.urls import include, path

from accounts import views, views_manager, views_customer


urlpatterns = [

    # Views
    path('connexion/', views.connexion_view, name='connexion'),
    path('inscription/', views.inscription_view, name='inscription'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('profil/', views.profil_view, name='profil'),
    path('edit-profil/', views.edit_profile, name='edit-profil'),

    # Views_Customer
    path('tableau-de-bord/', views_customer.customer_dashboard, name='customer-dash'),
    path('reservations/', views_customer.mes_reservations, name='reservations'),
    path('reservations/<str:token>/',
         views_customer.detail_reservation, name='reservation'),
    path('reservations/<str:token>/annuler', views_customer.annul_reservation,
         name='annul_reservation'),
    path('paiements/', views_customer.mes_paiements, name='paiements'),
    path('paiements/<str:token>/', views_customer.detail_paiement, name='paiement'),

    # Views_Manager
    path('manager/hotel', views_manager.manager_hotel, name='manager-hotel'),
    path('manager/tableau-de-bord/',
         views_manager.manager_dashboard, name='manager-dash'),
    path('manager/chambres', views_manager.manager_chambres,
         name='manager-chambres'),
    path('manager/chambres/ajouter-une-chambre',
         views_manager.add_room, name='add-room'),
    path('manager/chambres/ajouter-une-reservation',
         views_manager.add_booking, name='add-booking'),
    path('manager/chambres/<int:id>',
         views_manager.manager_chambre, name='manager-chambre'),
    path('manager/reservations', views_manager.manager_reservations,
         name='manager-reservations'),
    path('manager/reservations/verification/', views_manager.check_booking,
         name='check-booking'),
    path('manager/reservations/<str:token>/', views_manager.manager_reservation,
         name='manager-reservation'),
    path('manager/reservations/<str:token>/annuler', views_manager.annul_reservation,
         name='manager-annul-reservation'),
    path('manager/paiements/',
         views_manager.mes_paiements, name='manager-paiements'),
    path('manager/paiements/<str:token>/',
         views_manager.detail_pay, name='manager-pay'),
    path('manager/chambre/<int:id>/supprimer',
         views_manager.delete_room, name='delete-room'),
    path('manager/chambre/<int:id>/supprimer/confirmation',
         views_manager.delete_room_confirm, name='delete-room-confirm'),

]
