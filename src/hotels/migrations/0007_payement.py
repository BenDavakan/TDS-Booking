# Generated by Django 4.0.4 on 2022-07-02 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0006_alter_image_chambre_image_alter_image_hotel_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotels.reservation')),
            ],
        ),
    ]
