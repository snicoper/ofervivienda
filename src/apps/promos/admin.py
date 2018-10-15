from django.contrib import admin

from .models import Promo


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ('code', 'create_at', 'expire_at', 'active')
