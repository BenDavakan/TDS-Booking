# Generated by Django 4.0.4 on 2022-06-13 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0013_rename_cartegorie_category_rename_nom_category_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chambre',
            old_name='Category',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='chambre',
            old_name='nbr_lit',
            new_name='nbr_bed',
        ),
        migrations.RenameField(
            model_name='chambre',
            old_name='numero',
            new_name='number',
        ),
        migrations.RenameField(
            model_name='hotel',
            old_name='nbr_etoile',
            new_name='star_nbr',
        ),
    ]
