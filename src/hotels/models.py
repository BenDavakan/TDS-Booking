from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from django.core.validators import FileExtensionValidator

# Create your models here.


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    description = models.TextField(blank=True)
    tel_1 = models.CharField(max_length=100)
    tel_2 = models.IntegerField(blank=True, null=True)
    email = models.EmailField()
    adress = models.CharField(max_length=100, blank=True, null=True)
    star_nbr = models.PositiveIntegerField()
    ville = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    video = models.FileField(upload_to='videos_uploaded', null=True, blank=True,
                             validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("hotel", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now=True, blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name


class Chambre(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(blank=True)
    description = models.TextField(blank=True)
    number = models.IntegerField()
    overnight = models.DecimalField(max_digits=10, decimal_places=0)
    area = models.PositiveIntegerField()
    category = models.ForeignKey(
        Category, related_name='categorie', on_delete=models.CASCADE)
    hotel = models.ForeignKey(
        Hotel, related_name='hotel', on_delete=models.CASCADE)
    beds = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    video = models.FileField(upload_to='videos_uploaded', null=True, blank=True,
                             validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("chambre", kwargs={"number": self.number})

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    add_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    STATUS = [
        ('EC', 'En cours'),
        ('AN', 'Annulé'),
        ('P', 'Payé'),
    ]
    status = models.CharField(choices=STATUS, max_length=200, default='EC')


class Payement(models.Model):
    montant = models.PositiveIntegerField()
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)


class Equipement(models.Model):
    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE)
    add_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class Image_Hotel(models.Model):
    name = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="images/", validators=[
                              FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'webp'])])
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class Image_Chambre(models.Model):
    name = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="images/", validators=[
                              FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'webp'])])
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
