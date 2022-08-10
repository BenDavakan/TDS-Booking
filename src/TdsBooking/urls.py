""" TdsBooking URL Configuration

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
from hotels.views import transition
from TdsBooking import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls, name='tds'),
    path('', views.home_view, name='home'),
    path('contact/', views.contact_view, name='contact'),
    path('hotels/', include("hotels.urls"), name='hotels'),
    path('compte/', include('django.contrib.auth.urls')),
    path('compte/', include("accounts.urls"), name='accounts'),
    path('a-propos/', views.a_propos_view, name='a-propos'),


    path('transition/<int:number>/<str:type>/', transition, name='transition'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
