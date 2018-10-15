from django.utils import timezone
from django.utils.crypto import get_random_string

from payments.models import PaymentIpn
from promos.forms import PromoValidateCodeForm

from .base_promos import BasePromoTest


class PromoValidateCodeFormTest(BasePromoTest):

    def setUp(self):
        super().setUp()
        self.promo = self.promo_model.objects.create(
            payment_promo=PaymentIpn.ANUNCIO
        )
        self.form_data = {'code': self.promo.code}
        self.form = PromoValidateCodeForm(data=self.form_data)

    def test_form_valid(self):
        """Comprueba un form valido."""
        self.assertTrue(self.form.is_valid())

    def test_promo_invalid(self):
        """Inserta un código no valido."""
        new_code = get_random_string(length=12)
        form = PromoValidateCodeForm(data={'code': new_code})

        self.assertFalse(form.is_valid())

    def test_codigo_expirado(self):
        """Un código que ha expirado no es valido."""
        promo = self.promo_model.objects.create(
            payment_promo=PaymentIpn.ANUNCIO
        )
        promo.expire_at = timezone.now() - timezone.timedelta(days=1)
        promo.save()
        form = PromoValidateCodeForm(data={'code': promo.code})

        self.assertFalse(form.is_valid())

    def test_code_ya_usado_no_es_valido(self):
        """Un código solo es de un uso."""
        self.promo.active = True
        self.promo.save()
        form = PromoValidateCodeForm(data=self.form_data)

        self.assertFalse(form.is_valid())
