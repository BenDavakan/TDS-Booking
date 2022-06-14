"""TdsBooking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from TdsBooking import settings
from hotels.views import hotel_detail, chambre_detail
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view),
    path('contact/', views.contact_view),
    path('hotels/', include("hotels.urls")),
    path('hotels/<str:slug>/', hotel_detail, name='hotel'),
    path('hotels/<str:slug>/chambre/<int:number>/', chambre_detail, name='chambre'),
    path('connexion/', views.connexion_view),
    
    path('inscription/', views.inscription_view),
    path('a-propos/', views.a_propos_view),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
