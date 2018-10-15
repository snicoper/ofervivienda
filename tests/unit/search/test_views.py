from django.core.paginator import UnorderedObjectListWarning
from django.urls import reverse

from search import forms as search_forms

from .base_search import BaseSearchTest


class IndexSearchViewTest(BaseSearchTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'home_page'
        self.url = reverse(self.urlconf)
        self.response = self.client.get(self.url)

    def test_home_page_status_code_200(self):
        """home_page es la pagina principal del sitio."""
        self.assertEqual(self.response.status_code, 200)

    def test_usuario_login_status_code_200(self):
        """Usuario anónimo también status_code 200."""
        self.assertTrue(self.login())
        response = self.client.get(self.url)

        self.assertTrue(response.status_code, 200)

    def test_template_usado(self):
        """Comprueba el template usado."""
        self.assertTemplateUsed(self.response, 'search/index.html')


class SearchFiltersViewTest(BaseSearchTest):
    """La view tiene 2 URLConf asociadas.

    search:search y search:search_category.

    En caso de search:search, la categoría por defecto sera 'piso', en caso de
    search:search_category sera la categoría si existe o Http404 en caso de no
    existir.

    Algunos test cuando es el .client.get(url, data=form_data) lanza el warning
    UnorderedObjectListWarning.
    Se envuelve en un self.assertWarns.
    """
    def setUp(self):
        super().setUp()
        self.urlconf = 'search:search'
        self.urlconf_category = 'search:search_category'
        self.url = reverse(self.urlconf)
        self.response = self.client.get(self.url)

    def test_status_code_200(self):
        """Prueba search:search."""
        self.assertEqual(self.response.status_code, 200)

    def test_search_category_status_code_200(self):
        """Prueba search:search_category."""
        self.assertEqual(self.response.status_code, 200)

    def test_usuario_login_status_code_200(self):
        """Usuario anónimo también status_code 200."""
        self.assertTrue(self.login())
        response = self.client.get(self.url)

        self.assertTrue(response.status_code, 200)

    def test_category_not_exists_status_code_404(self):
        """Si no existe una categoría, Http404."""
        response = self.client.get(
            reverse('search:search_category', kwargs={'category': 'noexiste'})
        )

        self.assertEqual(response.status_code, 404)

    def test_template_usado(self):
        """Comprueba el template usado."""
        self.assertTemplateUsed(self.response, 'search/search_filters.html')

    def test_urlconf_sin_category_pone_piso_por_default(self):
        """Con search:search pone por defecto como categoría piso."""
        category_name = self.response.context['category_name']

        self.assertEqual(category_name, 'Piso')

    def test_form_class(self):
        """Prueba la instancia del form."""
        form = self.response.context['form']

        # Form por defecto.
        self.assertIsInstance(form, search_forms.SearchPisoForm)

        # Form para casas.
        # Ya no prueba mas por que get_form_class, esta probado en test_forms.py
        response = self.client.get(
            reverse(self.urlconf_category, kwargs={'category': 'casa'})
        )
        form = response.context['form']

        # Form por defecto.
        self.assertIsInstance(form, search_forms.SearchCasaForm)

    def test_context_data(self):
        """Prueba los datos de contexto."""
        self.assertIn('anuncio_list', self.response.context)
        self.assertIn('form', self.response.context)
        self.assertIn('category_name', self.response.context)

    def test_anade_al_form_campo_q(self):
        """En la vista añade el campo q."""
        self.assertTrue(self.response.context['form']['q'])

    def test_anade_a_initial_category(self):
        """Al obtener el form en get_form, añade la categoría en form.initial."""
        initial = self.response.context['form'].initial['category']

        self.assertEqual(initial, 'PISO')

    def test_form_post(self):
        """Prueba el form en post.

        Esta parte en muy sensible a los fixtures anuncios.json

        La validación del form, ya esta en test_forms.py
        """
        form_data = {
            'category': 'PISO',
            'q': 'granollers'
        }
        with self.assertWarns(UnorderedObjectListWarning):
            response = self.client.get(self.url, data=form_data)

        self.assertEqual(response.status_code, 200)
        items = response.context['anuncio_list']

        # Items devueltos
        self.assertEqual(items.count(), 3)

    def test_anuncios_active_false_no_los_muestra(self):
        """Los anuncios active=False no los muestra en los resultados."""
        anuncio_list = self.anuncio_model.objects.published(category='PISO', city='Granollers')[0]
        anuncio_list.active = False
        anuncio_list.save()
        anuncio_list = self.anuncio_model.objects.published(category='PISO', city='Granollers')

        self.assertTrue(anuncio_list.count(), 2)
        form_data = {
            'category': 'PISO',
            'q': 'Granollers'
        }
        with self.assertWarns(UnorderedObjectListWarning):
            response = self.client.get(self.url, data=form_data)
        items = response.context['anuncio_list']

        # Items devueltos
        self.assertEqual(items.count(), 2)


class SearchMapViewTest(BaseSearchTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'search:map'
        self.url = reverse(self.urlconf, kwargs={'category': 'piso'})
        self.response = self.client.get(self.url)

    def test_status_code_200(self):
        """Prueba search:search."""
        self.assertEqual(self.response.status_code, 200)

    def test_search_category_status_code_200(self):
        """Prueba search:map."""
        self.assertEqual(self.response.status_code, 200)

    def test_usuario_login_status_code_200(self):
        """Usuario anónimo también status_code 200."""
        self.assertTrue(self.login())
        response = self.client.get(self.url)

        self.assertTrue(response.status_code, 200)

    def test_category_not_exists_status_code_404(self):
        """Si no existe una categoría, Http404."""
        response = self.client.get(
            reverse('search:map', kwargs={'category': 'noexiste'})
        )

        self.assertEqual(response.status_code, 404)

    def test_template_usado(self):
        """Comprueba el template usado."""
        self.assertTemplateUsed(self.response, 'search/search_map.html')

    def test_urlconf_sin_category_pone_piso_por_default(self):
        """Con search:map pone por defecto como categoría_name piso."""
        category_name = self.response.context['category_name']

        self.assertEqual(category_name, 'PISO')

    def test_form_class(self):
        """Prueba la instancia del form."""
        form = self.response.context['form']

        # Form por defecto.
        self.assertIsInstance(form, search_forms.SearchPisoForm)

        # Form para casas.
        # Ya no prueba mas por que get_form_class, esta probado en test_forms.py
        response = self.client.get(
            reverse(self.urlconf, kwargs={'category': 'casa'})
        )
        form = response.context['form']

        # Form por defecto.
        self.assertIsInstance(form, search_forms.SearchCasaForm)

    def test_context_data(self):
        """Prueba los datos de contexto."""
        self.assertIn('form', self.response.context)
        self.assertIn('title', self.response.context)
        self.assertIn('category_name', self.response.context)

    def test_anade_a_initial_category(self):
        """Al obtener el form en get_form, añade la categoría en form.initial."""
        initial = self.response.context['form'].initial['category']

        self.assertEqual(initial, 'PISO')
