from django.db import IntegrityError

from alerts.models import AlertAnuncio
from anuncios.models import AbstractAnuncioModel
from localization.models import AbstractLocationModel
from tests.unit.base_test import BaseTestCase


class AlertAnuncioTest(BaseTestCase):
    """Solo se prueba AlertAnuncio, el resto son probados en anuncios."""

    def setUp(self):
        super().setUp()
        self.alert = AlertAnuncio.objects.create(
            owner=self.user,
            description='alert test'
        )

    def test_es_subclase_de_AbstractAnuncioModel(self):
        """Comprueba la herencia."""
        self.assertIsInstance(self.alert, AbstractAnuncioModel)
        self.assertIsInstance(self.alert, AbstractLocationModel)
        self.assertIsInstance(self.alert, AlertAnuncio)

    def test_no_permite_misma_descripcion(self):
        """A un mismo usuario, no puede poner 2 veces la misma descripción."""
        with self.assertRaises(IntegrityError):
            AlertAnuncio.objects.create(
                owner=self.user,
                description='alert test'
            )

    def test_perico_puede_crear_alert_misma_desc(self):
        """El usuario perico puede crear una alerta con descripción igual.

        perico crea una alerta con una descripción igual a la de snicoper
        y no da error.
        """
        # Usuario perico, creara el mismo Alert
        perico = self.user_model.objects.get(pk=2)
        alert = AlertAnuncio.objects.create(
            owner=perico,
            description='alert test'
        )

        self.assertTrue(alert)

    def test_str(self):
        """Obtiene el username."""
        self.assertEqual(str(self.alert), self.user.username)
