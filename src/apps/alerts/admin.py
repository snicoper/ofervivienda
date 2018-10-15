from django.contrib import admin

from . import models


class AlertAdminMixin(object):
    list_display = (
        '__str__',
        'id',
        'owner',
        'get_category_display',
        'create_at',
        'update_at',
        'active',
    )


@admin.register(models.AlertAnuncio)
class AlertAdmin(AlertAdminMixin, admin.ModelAdmin):
    pass


@admin.register(models.AlertPiso)
class AlertPisoAdmin(AlertAdminMixin, admin.ModelAdmin):
    pass


@admin.register(models.AlertCasa)
class AlertCasaAdmin(AlertAdminMixin, admin.ModelAdmin):
    pass


@admin.register(models.AlertApartamento)
class AlertApartamentoAdmin(AlertAdminMixin, admin.ModelAdmin):
    pass


@admin.register(models.AlertHabitacion)
class AlertHabitacionAdmin(AlertAdminMixin, admin.ModelAdmin):
    pass


@admin.register(models.AlertTerreno)
class AlertTerrenoAdmin(AlertAdminMixin, admin.ModelAdmin):
    pass


@admin.register(models.AlertParking)
class AlertParkingAdmin(AlertAdminMixin, admin.ModelAdmin):
    pass


@admin.register(models.AlertIndustrial)
class AlertIndustrialAdmin(AlertAdminMixin, admin.ModelAdmin):
    pass


@admin.register(models.AlertLocal)
class AlertLocalAdmin(AlertAdminMixin, admin.ModelAdmin):
    pass
