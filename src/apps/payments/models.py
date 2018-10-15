from django.conf import settings
from django.db import models


class PaymentIpn(models.Model):
    """Datos de pago."""
    PREMIUM1 = 'PREMIUM1'
    PREMIUM3 = 'PREMIUM3'
    PREMIUM6 = 'PREMIUM6'
    PREMIUM12 = 'PREMIUM12'
    ANUNCIO = 'ANUNCIO'

    PAYMENT_CHOICES = (
        (PREMIUM1, '1 Mes Premium'),
        (PREMIUM3, '3 Meses Premium'),
        (PREMIUM6, '6 Meses Premium'),
        (PREMIUM12, '1 Año Premium'),
        (ANUNCIO, 'Anuncio Premium'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments_ipn_user'
    )
    item_name = models.CharField(
        verbose_name='Tipo pago value',
        max_length=127
    )
    item_number = models.CharField(
        verbose_name='Tipo pago clave',
        max_length=127
    )
    invoice = models.CharField(
        verbose_name='ID Factura',
        max_length=127,
        unique=True
    )
    txn_id = models.CharField(
        max_length=255
    )
    payment_status = models.CharField(
        max_length=10
    )
    total_amount = models.FloatField(
        verbose_name='Cantidad pagada',
        default=0.0
    )
    receiver_amount = models.FloatField(
        verbose_name='Cantidad recibida',
        default=0.0
    )
    post_data = models.TextField(
        verbose_name='Datos retornados por PayPal'
    )
    payment_date = models.DateTimeField(
        auto_now_add=True
    )
