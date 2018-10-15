from django.test import override_settings
from django.utils import timezone

from payments.models import PaymentIpn
from promos import settings as promos_settings

from .base_promos import BasePromoTest


@override_settings(USE_TZ=False)
class PromoTest(BasePromoTest):

    def setUp(self):
        super().setUp()
        self.data = {'payment_promo': PaymentIpn.PREMIUM1}
        self.promo = self.promo_model.objects.create(**self.data)
        self.user = self.user_model.objects.get(pk=1)

    def test_create_promo(self):
        """Crea un código de promoción y prueba varias opciones."""
        self.assertEqual(self.promo_model.objects.count(), 1)

    def test_90_dias_expiracion_por_defecto(self):
        """Por defecto expira en promos_settings.PROMO_EXPIRE_DAYS días."""
        expire_at = timezone.now() + timezone.timedelta(days=promos_settings.PROMO_EXPIRE_DAYS)

        self.assertEqual(self.promo.expire_at.year, expire_at.year)
        self.assertEqual(self.promo.expire_at.month, expire_at.month)
        self.assertEqual(self.promo.expire_at.day, expire_at.day)

    def test_active_False_por_defecto(self):
        """Por defecto active es False."""
        self.assertFalse(self.promo.active)

    def test_campo_pyment_promo(self):
        """Prueba el campo payment_promo."""
        self.assertEqual(self.promo.payment_promo, PaymentIpn.PREMIUM1)

    def test_active_promo_PREMIUM3(self):
        """Prueba PaymentIpn.PREMIUM3 al activar el código."""
        promo = self.promo_model.objects.create(payment_promo=PaymentIpn.PREMIUM3)

        self.assertTrue(promo.active_promo(self.user))

    def test_active_promo_PREMIUM6(self):
        """Prueba PaymentIpn.PREMIUM6 al activar el código."""
        promo = self.promo_model.objects.create(payment_promo=PaymentIpn.PREMIUM6)

        self.assertTrue(promo.active_promo(self.user))

    def test_active_promo_PREMIUM12(self):
        """Prueba PaymentIpn.PREMIUM12 al activar el código."""
        promo = self.promo_model.objects.create(payment_promo=PaymentIpn.PREMIUM12)

        self.assertTrue(promo.active_promo(self.user))

    def test_active_promo_ANUNCIO(self):
        """Prueba PaymentIpn.ANUNCIO al activar el código."""
        promo = self.promo_model.objects.create(payment_promo=PaymentIpn.ANUNCIO)

        self.assertTrue(promo.active_promo(self.user))

    def test_active_promo_expirado(self):
        """Prueba active_promo, si esta expirado, devuelve False."""
        self.promo.expire_at = timezone.now() - timezone.timedelta(days=1)
        self.promo.save()

        self.assertFalse(self.promo.active_promo(self.user))

    def test_active_promo_actualiza_usuario(self):
        """Al usuario se le actualiza cuenta premium 1 mes."""
        # Comprueba que el usuario, no tiene cuenta premium.
        self.assertFalse(self.user.is_premium)

        # Asignar código de promoción al usuario.
        self.assertTrue(self.promo.active_promo(self.user))
        self.promo.save()

        # El usuario ahora es premium.
        user = self.user_model.objects.get(pk=1)
        self.assertTrue(user.is_premium)

        # La promoción se ha establecido como activa.
        self.assertTrue(self.promo.active)

    def test_payment_promo_no_implementado(self):
        """Si en PaymentIpn.PAYMENT_CHOICES se implementa un nuevo tipo, si no
        se añade en Promo.payment_promo lanzara un NotImplementedError.
        """
        original_payment_choices = PaymentIpn.PAYMENT_CHOICES
        PaymentIpn.PAYMENT_CHOICES += (('OBRANUEVA', 'obranueva'),)
        promo = self.promo_model.objects.create(payment_promo='OBRANUEVA')

        self.assertEqual(self.promo_model.objects.count(), 2)

        with self.assertRaises(NotImplementedError):
            promo.active_promo(self.user)

        # IMPORTANTE: Restablecer valor predeterminado.
        PaymentIpn.PAYMENT_CHOICES = original_payment_choices
