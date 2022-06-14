from xml.dom.pulldom import parseString
from django.contrib import admin

# Register your models here.
from hotels.models import Category, Chambre, Hotel, Image_Chambre, Image_Hotel


class ImageHotel(admin.StackedInline):
    model = Image_Hotel


class ImageChambre(admin.StackedInline):
    model = Image_Chambre


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "email",
    )
    search_fields = ('name',)

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
        "category"
    )
    
    search_fields = ('name','hotel__field1')
    
    list_editable = ('overnight',)

    inlines = [ImageChambre]

    class Meta:
        model = Chambre


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )
