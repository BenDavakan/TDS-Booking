# Generated by Django 4.0.4 on 2022-08-15 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chambre',
            name='capacity',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
