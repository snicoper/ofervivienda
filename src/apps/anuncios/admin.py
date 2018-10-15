from django.contrib import admin

from gallery.models import ImageAnuncio

from . import models


class ImageAnuncioInline(admin.StackedInline):
    model = ImageAnuncio


class AnuncioAdminMixin(object):
    inlines = [
        ImageAnuncioInline,
    ]
    list_display = (
        '__str__',
        'id',
        'owner',
        'get_category_display',
        'get_type_anuncio_display',
        'get_estado_inmueble_display',
        'is_premium',
        'active',
        'create_at_short_time',
        'update_at_short_time',
    )

    def create_at_short_time(self, obj):
        return self._short_time(obj.create_at)

    def update_at_short_time(self, obj):
        return self._short_time(obj.update_at)

    def _short_time(self, timefield):
        return timefield.strftime('%d-%m-%Y')


@admin.register(models.Anuncio)
class AnuncioAdmin(AnuncioAdminMixin, admin.ModelAdmin):
    """Global Anuncio para la eliminación desde el admin.

    Si se intenta eliminar un anuncio por su categoría, el anuncio continuara en
    la db y por lo tanto lo mostrara.
    Para eliminar un anuncio, se ha de hacer con este register.
    """
    pass


@admin.register(models.AnuncioPiso)
class AnuncioPisoAdmin(AnuncioAdminMixin, admin.ModelAdmin):
    pass


@admin.register(models.AnuncioCasa)
class AnuncioCasaAdmin(AnuncioAdminMixin, admin.ModelAdmin):
    pass


@admin.register(models.AnuncioApartamento)
class AnuncioApartamentoAdmin(AnuncioAdminMixin, admin.ModelAdmin):
    pass


@admin.register(models.AnuncioHabitacion)
class AnuncioHabitacionAdmin(AnuncioAdminMixin, admin.ModelAdmin):
    pass


@admin.register(models.AnuncioTerreno)
class AnuncioTerrenoAdmin(AnuncioAdminMixin, admin.ModelAdmin):
    pass


@admin.register(models.AnuncioParking)
class AnuncioParkingAdmin(AnuncioAdminMixin, admin.ModelAdmin):
    pass


@admin.register(models.AnuncioIndustrial)
class AnuncioIndustrialAdmin(AnuncioAdminMixin, admin.ModelAdmin):
    pass


@admin.register(models.AnuncioLocal)
class AnuncioLocalAdmin(AnuncioAdminMixin, admin.ModelAdmin):
    pass
