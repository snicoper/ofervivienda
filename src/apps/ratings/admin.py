from django.contrib import admin

from .models import Ratio


@admin.register(Ratio)
class RatioAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'score')
    raw_id_fields = ('anuncio',)
