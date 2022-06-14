#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TdsBooking.settings')

import django
django.setup()

import random

from hotels.models import Category, Chambre, Hotel
from faker import Faker

fake = Faker(locale="fr-FR")

hotels = ['Novotel', 'Link Hôtel', 'Golden Tulip', 'Azalai Hôtel', 'Hôtel du Port', 'Sun Beach Hôtel', 'Hôtel du Lac', 'Nobila Airport Hôtel',
          'Tahiti Hôtel', 'Hotel Mainson Rouge', 'Hotel de la Dispora', 'Villa San Miguel', 'Lagoon Residence', 'La Brume Joyeuse']
etoiles = ['1', '2', '3', '4', '5', '6', '7', '8']
villes = ['Cotonou', 'Lokossa', 'Ouidah', 'Parakou',
          'Djougou', 'Abomey-Calavi', 'Bohicon', 'Abomey']


def add_hotel(N):
    for i in range(N):
        h = Hotel.objects.get_or_create(
            name=hotels[i], description=fake.paragraph(), tel_1=fake.phone_number(), email=fake.email(),adress=fake.address(), nbr_etoile=random.choice(etoiles), ville=random.choice(villes),)[0]
        # h.save()
        # return h


categories = ['Suite', 'Standard', 'VIP']


def add_cartegorie(N):
    for i in range(N):
        c = Category.objects.get_or_create(
            name=categories[i], description=fake.paragraph())[0]
        # c.save()
        # return c


def populate(N):
        
    for i in range(N):
        hotel = random.choice(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
        categorie = random.choice(['1', '2', '3'])

        chambre = Chambre.objects.get_or_create(name=fake.company(), description=fake.paragraph(), numero=fake.random_int(min=1, max=100), overnight=fake.random_int(min=15000, max=900000), area=fake.random_int(min=45, max=100), category_id=categorie, hotel_id=hotel, nbr_lit=fake.random_int(min=1, max=3))[0]


if __name__ == '__main__':
    print("Populating Script!")
    add_hotel(13)
    # add_cartegorie(3)
    populate(30)
    print("Populating Complete!")
