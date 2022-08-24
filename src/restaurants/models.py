from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.


class Restaurant(models.Model):
    nom = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    description = models.TextField(blank=True)
    tel_1 = models.IntegerField()
    tel_2 = models.IntegerField(blank=True, null=True)
    email = models.EmailField()
    nbr_etoile = models.PositiveIntegerField()

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse("restaurant", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.nom)

        super().save(*args, **kwargs)
