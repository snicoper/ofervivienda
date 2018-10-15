from anuncios.models import AnuncioHabitacion
from tests.unit.base_test import BaseTestCase


class AnuncioConstantesTest(BaseTestCase):
    """Constantes en los modelos, para los campos choices."""

    def test_category(self):
        """Prueba CATEGORY_CHOICES."""
        # KEYS
        self.assertEqual(self.anuncio_model.PISO, 'PISO')
        self.assertEqual(self.anuncio_model.CASA, 'CASA')
        self.assertEqual(self.anuncio_model.APARTAMENTO, 'APARTAMENTO')
        self.assertEqual(self.anuncio_model.HABITACION, 'HABITACION')
        self.assertEqual(self.anuncio_model.TERRENO, 'TERRENO')
        self.assertEqual(self.anuncio_model.PARKING, 'PARKING')
        self.assertEqual(self.anuncio_model.INDUSTRIAL, 'INDUSTRIAL')
        self.assertEqual(self.anuncio_model.LOCAL, 'LOCAL')

        # VALUES
        category_list = {k: v for k, v in self.anuncio_model.CATEGORY_CHOICES}

        self.assertEqual(category_list.get(self.anuncio_model.PISO), 'Piso')
        self.assertEqual(category_list.get(self.anuncio_model.CASA), 'Casa')
        self.assertEqual(category_list.get(self.anuncio_model.APARTAMENTO), 'Apartamento')
        self.assertEqual(category_list.get(self.anuncio_model.HABITACION), 'Habitacion')
        self.assertEqual(category_list.get(self.anuncio_model.TERRENO), 'Terreno')
        self.assertEqual(category_list.get(self.anuncio_model.PARKING), 'Parking')
        self.assertEqual(category_list.get(self.anuncio_model.INDUSTRIAL), 'Nave Industrial')
        self.assertEqual(category_list.get(self.anuncio_model.LOCAL), 'Local')

    def test_type_anuncios(self):
        """Prueba TYPE_ANUNCIO_CHOICES."""
        # KEYS
        self.assertEqual(self.anuncio_model.VENTA, 'VENTA')
        self.assertEqual(self.anuncio_model.ALQUILER, 'ALQUILER')

        # VALUES
        category_list = {k: v for k, v in self.anuncio_model.TYPE_ANUNCIO_CHOICES}

        self.assertEqual(category_list.get(self.anuncio_model.VENTA), 'Venta')
        self.assertEqual(category_list.get(self.anuncio_model.ALQUILER), 'Alquiler')

    def test_estado_inmueble(self):
        """Prueba ESTADO_INMUEBLE_CHOICES."""
        # KEYS
        self.assertEqual(self.anuncio_model.OBRANUEVA, 'OBRANUEVA')
        self.assertEqual(self.anuncio_model.BUENESTADO, 'BUENESTADO')
        self.assertEqual(self.anuncio_model.AREFORMAR, 'AREFORMAR')

        # VALUES
        category_list = {k: v for k, v in self.anuncio_model.ESTADO_INMUEBLE_CHOICES}

        self.assertEqual(category_list.get(self.anuncio_model.OBRANUEVA), 'Obra nueva')
        self.assertEqual(category_list.get(self.anuncio_model.BUENESTADO), 'Buen estado')
        self.assertEqual(category_list.get(self.anuncio_model.AREFORMAR), 'A reformar')

    def test_currencies(self):
        """Prueba CURRENCY_SYMBOLS."""
        # KEYS
        self.assertEqual(self.anuncio_model.EUR, 'EUR')
        self.assertEqual(self.anuncio_model.USD, 'USD')
        self.assertEqual(self.anuncio_model.GBP, 'GBP')

        # VALUES
        currency_list = {k: v for k, v in self.anuncio_model.CURRENCY_SYMBOLS}

        self.assertEqual(currency_list.get(self.anuncio_model.EUR), '€')
        self.assertEqual(currency_list.get(self.anuncio_model.USD), '$')
        self.assertEqual(currency_list.get(self.anuncio_model.GBP), '£')

    def test_habitacion_genero_choices(self):
        """Prueba src/apps/anuncios/mixins/models.AnuncioHabitacionMixin."""
        self.assertEqual(AnuncioHabitacion.CHICOCHICA, 'CHICOCHICA')
        self.assertEqual(AnuncioHabitacion.CHICO, 'CHICO')
        self.assertEqual(AnuncioHabitacion.CHICA, 'CHICA')

        genero_list = {k: v for k, v in AnuncioHabitacion.GENERO_CHOICES}

        self.assertEqual(genero_list.get(AnuncioHabitacion.CHICOCHICA), 'Chicos y Chicas')
        self.assertEqual(genero_list.get(AnuncioHabitacion.CHICO), 'Chicos')
        self.assertEqual(genero_list.get(AnuncioHabitacion.CHICA), 'Chicas')
