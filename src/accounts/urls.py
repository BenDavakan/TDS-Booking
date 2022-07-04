from django.urls import include, path

from accounts import views


urlpatterns = [

    path('connexion/', views.connexion_view, name='connexion'),
    path('inscription/', views.inscription_view, name='inscription'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),

]
