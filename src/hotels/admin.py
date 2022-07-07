from xml.dom.pulldom import parseString
from django.contrib import admin

# Register your models here.
from hotels.models import Availability, Category, Chambre, Equipement, Hotel, Image_Chambre, Image_Hotel, Reservation, Ville


class ImageHotel(admin.StackedInline):
    model = Image_Hotel


class ImageChambre(admin.StackedInline):
    model = Image_Chambre


class EquipChambre(admin.StackedInline):
    model = Equipement


@admin.register(Ville)
class VilleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "pays",
    )


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "ville",
        "email",
        "tel_1",

    )
    search_fields = ('name', 'ville')

    inlines = [ImageHotel]

    class Meta:
        model = Hotel


@admin.register(Chambre)
class ChambreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "hotel",
        "number",
        "overnight",
        "capacity",
        "category",

    )

    search_fields = ('number', 'hotel__name', 'category__name')

    list_editable = ('overnight',)

    inlines = [ImageChambre, EquipChambre]

    class Meta:
        model = Chambre


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = (
        "chambre",
        "check_in",
        "check_out",
        "status",
    )


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "chambre",
        "check_in",
        "check_out",
        "add_at",
        "status",
    )


@admin.register(Equipement)
class EquipementAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "number",
        "chambre",
        "add_at",
    )
