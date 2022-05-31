from xml.dom.pulldom import parseString
from django.contrib import admin

# Register your models here.
from hotels.models import Cartegorie, Chambre, Hotel, Image


class ImageAdmin(admin.StackedInline):
    model = Image


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = (
        "nom",
        "description",
        "email",
    )

    inlines = [ImageAdmin]

    class Meta:
        model = Hotel


@admin.register(Chambre)
class ChambreAdmin(admin.ModelAdmin):
    list_display = (
        "nom",
    )

    inlines = [ImageAdmin]

    class Meta:
        model = Chambre


@admin.register(Cartegorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = (
        "nom",
    )
