# Generated by Django 4.0.4 on 2022-08-17 14:59

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0004_alter_image_hotel_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chambre',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]