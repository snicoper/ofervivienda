from django.contrib import admin

from .models import PaymentIpn


@admin.register(PaymentIpn)
class PaymentIpnAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'item_name',
        'txn_id',
        'invoice',
        'total_amount',
        'receiver_amount',
        'payment_date',
    )
