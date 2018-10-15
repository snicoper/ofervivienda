from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string

from payments.models import PaymentIpn

from .settings import PROMO_EXPIRE_DAYS


class Promo(models.Model):
    """Códigos de promoción.

    De momento, solo esta pensado un código, un solo uso.
    """
    code = models.CharField(
        max_length=12,
        blank=True,
        help_text='Se auto genera'
    )
    payment_promo = models.CharField(
        max_length=20,
        choices=PaymentIpn.PAYMENT_CHOICES
    )
    active = models.BooleanField(
        default=False
    )
    create_at = models.DateTimeField(
        verbose_name='Fecha creación',
        auto_now_add=True
    )
    expire_at = models.DateTimeField(
        verbose_name='Fecha expiración',
        blank=True,
        help_text='Por defecto {} días'.format(PROMO_EXPIRE_DAYS)
    )

    def save(self, *args, **kwargs):
        if not self.id:
            while True:
                code = get_random_string(length=12)
                if not Promo.objects.filter(code=code):
                    break
            self.code = code
            if not self.expire_at:
                # Fecha de expiración de PROMO_EXPIRE_DAYS.
                self.expire_at = timezone.now() + timezone.timedelta(days=PROMO_EXPIRE_DAYS)
        super().save(*args, **kwargs)

    def active_promo(self, user):
        """Poner el código de promoción como activo.

        Dependiendo de payment_promo, se le incrementa en la cuenta de usuario.
        Si esta expirado el código, devolverá False.
        Una vez usado, se ha de guardar el objeto Promo explícitamente.

        Args:
            user (User): Usuario que aplica el código.

        Returns:
            bool: True en caso de éxito, False en caso contrario.
        """
        if self.expire_at < timezone.now():
            return False
        if self.payment_promo == PaymentIpn.PREMIUM1:
            user.update_premium(1)
        elif self.payment_promo == PaymentIpn.PREMIUM3:
            user.update_premium(3)
        elif self.payment_promo == PaymentIpn.PREMIUM6:
            user.update_premium(6)
        elif self.payment_promo == PaymentIpn.PREMIUM12:
            user.update_premium(12)
        elif self.payment_promo == PaymentIpn.ANUNCIO:
            user.increase_anuncio()
        else:
            msg_error = '{} no implementado en {}.{}'.format(
                self.payment_promo,
                self.__class__.__name__,
                'active_promo()'
            )
            raise NotImplementedError(msg_error)
        user.save()
        self.active = True
        return True
