from django.urls import path
from .views import hotels_view

urlpatterns = [
    path('', hotels_view, name="hotels-index"),
]
