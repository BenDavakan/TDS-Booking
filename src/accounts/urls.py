from django.urls import include, path

from accounts import views


urlpatterns = [

    path('connexion/', views.connexion_view, name='connexion'),
    path('inscription/', views.inscription_view, name='inscription'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('profil/', views.profil_view, name='profil'),
    path('dashboard-admin/', views.dashboard_admin, name='dashboard_admin'),
    path('edit-profil/', views.edit_profile, name='edit-profil'),
    path('reservations/', views.mes_reservations, name='reservations'),
    path('manager/chambres', views.manager_chambres, name='manager-chambres'),
    path('manager/chambres/<int:number>',
         views.manager_chambre, name='manager-chambre'),
    path('reservations/<str:token>/',
         views.detail_reservation, name='reservation'),
    path('reservations/<int:id>/annuler', views.annul_reservation,
         name='annul_reservation'),
    path('paiements/', views.mes_paiements, name='paiements'),
    path('paiements/<str:token>/', views.detail_paiement, name='paiement'),




]
