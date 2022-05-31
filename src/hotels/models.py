from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.


class Hotel(models.Model):
    nom = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    description = models.TextField(blank=True)
    tel_1 = models.IntegerField()
    tel_2 = models.IntegerField(blank=True, null=True)
    email = models.EmailField()
    nbr_etoile = models.PositiveIntegerField()
    ville = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse("hotel", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.nom)

        super().save(*args, **kwargs)


class Service(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)


class Cartegorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom


class Chambre(models.Model):
    nom = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    description = models.TextField(blank=True)
    numero = models.IntegerField()
    nuite = models.DecimalField(max_digits=10, decimal_places=0)
    superficie = models.PositiveIntegerField()
    cartegorie = models.ForeignKey(Cartegorie, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    nbr_lit = models.PositiveIntegerField()

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.nom)

        super().save(*args, **kwargs)


class Equipement(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE)


class Image(models.Model):
    nom = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="images/")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE)
