from django.urls import reverse

from alerts import forms
from alerts.models import AlertAnuncio
from tests.unit.alerts.base_alerts import BaseTestAlerts


class AlertUserListViewTest(BaseTestAlerts):

    def setUp(self):
        super().setUp()
        self.urlconf = 'alerts:list'
        self.url = reverse(self.urlconf)
        self.login()
        self.response = self.client.get(self.url)

    def test_usuario_anonimo_redirecciona(self):
        """Un usuario anónimo lo redirecciona a settings.LOGIN_URL."""
        self.client.logout()
        response = self.client.get(self.url)
        expected_url = '{}?next={}'.format(
            reverse('authentication:login'),
            self.url
        )

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

    def test_status_code_200(self):
        """El status_code es 200 cuando esta logueado."""
        self.assertEqual(self.response.status_code, 200)

    def test_tamplete_usado(self):
        """Comprueba el template usado."""
        self.assertTemplateUsed(self.response, 'alerts/list.html')

    def test_context_object(self):
        """Prueba el nombre del context_object_name y el tipo."""
        context = self.response.context['alert_list']
        user = self.response.context['user']

        self.assertTrue(context)
        self.assertIsInstance(context[0], AlertAnuncio)
        self.assertEqual(context[0].owner, user)


class AlertDeleteViewTest(BaseTestAlerts):

    def setUp(self):
        super().setUp()
        self.urlconf = 'alerts:delete'
        self.url = reverse(self.urlconf, kwargs={'pk': 1})
        self.login()

    def test_login_required_y_status_code_200(self):
        """Requiere login y estatus code 200 con login."""
        self.client.logout()
        response = self.client.get(self.url)

        # Lanza un 404 si no esta logueado.
        self.assertEqual(response.status_code, 404)

        self.login()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_template(self):
        """Template usado."""
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'alerts/delete.html')

    def test_solo_owner_puede_eliminar_alert(self):
        """Solo el owner de la alert puede eliminarla."""
        login = self.client.login(username='perico', password='123')

        self.assertTrue(login)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_method_post_elimina_alert(self):
        """Elimina definitivamente la alerta."""
        self.assertEqual(AlertAnuncio.objects.count(), 2)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(AlertAnuncio.objects.count(), 1)

    def test_success_url(self):
        """Comprobar el redireccionamiento."""
        response = self.client.post(self.url, follow=True)
        request = response.context['request']

        self.assertEqual(request.get_full_path(), reverse('alerts:list'))

    def test_subclass(self):
        """Comprueba que sea la subclase del tipo correcto."""
        alert = AlertAnuncio.objects.get(pk=1)
        subclass_alert = AlertAnuncio.get_model_class(alert.category)

        self.assertTrue(subclass_alert.objects.get(pk=1))


class AlertsDeleteAllViewTest(BaseTestAlerts):

    def setUp(self):
        super().setUp()
        self.urlconf = 'alerts:delete_all'
        self.url = reverse(self.urlconf)
        self.login()

    def test_login_required_y_status_code_200(self):
        """Requiere login y estatus code 200 con login."""
        self.client.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

        self.login()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_template(self):
        """Template usado."""
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'alerts/delete_all.html')

    def test_status_code_post(self):
        """Comprueba el status_code de post y que elimine las alertas."""
        self.login()
        response = self.client.post(self.url, data={'delete_all': '1'}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('alerts:list'))
        self.assertEqual(AlertAnuncio.objects.count(), 1)


class AlertDetailsViewTest(BaseTestAlerts):

    def setUp(self):
        super().setUp()
        self.urlconf = 'alerts:details'
        self.url = reverse(self.urlconf, kwargs={'pk': 1})
        self.login()

    def test_login_required_y_status_code_200(self):
        """Requiere login y estatus code 200 con login."""
        self.client.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

        self.login()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_un_usuario_no_puede_ver_alertas_de_otro_usuario(self):
        """Un usuario no puede ver las alertas de otro cambiando la id en la URI."""
        self.login()
        response = self.client.get(self.urlconf, kwargs={'pk', 2})
        self.assertEqual(response.status_code, 404)

    def test_template(self):
        """Template usado."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'alerts/details.html')

    def test_subclass(self):
        """Comprueba que sea la subclase del tipo correcto."""
        alert = AlertAnuncio.objects.get(pk=1)
        subclass_alert = AlertAnuncio.get_model_class(alert.category)
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['alert'], subclass_alert)


class AlertCreateViewTest(BaseTestAlerts):

    def setUp(self):
        super().setUp()
        self.urlconf = 'alerts:create'
        self.alert = AlertAnuncio.objects.get(pk=1)
        self.url = reverse(self.urlconf, kwargs={'category': self.alert.category.lower()})
        self.login()

    def test_login_required_y_status_code_200(self):
        """Requiere login y estatus code 200 con login."""
        self.client.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

        self.login()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_un_usuario_no_puede_ver_alertas_de_otro_usuario(self):
        """Un usuario no puede ver las alertas de otro cambiando la id en la URI."""
        self.login()
        response = self.client.get(self.urlconf, kwargs={'pk', 2})
        self.assertEqual(response.status_code, 404)

    def test_template(self):
        """Template usado."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'alerts/alerts_form.html')

    def test_subclass(self):
        """Comprueba que sea la subclase del tipo correcto."""
        subclass_alert = forms.BaseAlertForm.get_form_class(self.alert.category)
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], subclass_alert)

    def test_comprueba_campos_initial(self):
        """Comprueba que tengan valores campos que lo requieran."""
        response = self.client.get(self.url)
        form = response.context['form']
        user = response.context['user']

        # owner ha de ser el mismo que usuario.
        self.assertEqual(form.initial['owner'], user.pk)

        # Comprueba category
        self.assertEqual(form.initial['category'], self.alert.category)

    def test_contexto(self):
        """Comprueba el contexto requerido."""
        response = self.client.get(self.url)
        context = response.context

        # Titulo para la pagina
        self.assertEqual(context['title'], 'Añadir nueva alerta ')

        # Nombre del botón type submit.
        self.assertEqual(context['btn_form_name'], 'Crear')

        # Nombre de la categoría.
        choices_values = {k: v for k, v in AlertAnuncio.CATEGORY_CHOICES}
        self.assertEqual(
            context['category_name'],
            choices_values[self.alert.category]
        )

    def test_crea_alerta(self):
        """Crea una alerta y redirecciona."""
        initial_items = AlertAnuncio.objects.count()
        response = self.client.post(
            reverse('alerts:create', kwargs={'category': self.form_data['category'].lower()}),
            data=self.form_data,
            follow=True
        )

        # Comprueba que se ha creado la alerta.
        actual_alerts = AlertAnuncio.objects.count()
        self.assertGreater(actual_alerts, initial_items)

        # El ultimo id es igual a la cantidad de alertas.
        last_insert = AlertAnuncio.objects.last()
        self.assertEqual(last_insert.id, actual_alerts)

        # Redirecciona a details
        self.assertRedirects(
            response=response,
            expected_url=reverse('alerts:details', kwargs={'pk': 3}),
            status_code=302,
            target_status_code=200
        )


class AlertUpdateViewTest(BaseTestAlerts):

    def setUp(self):
        super().setUp()
        self.urlconf = 'alerts:update'
        self.alert = AlertAnuncio.objects.get(pk=1)
        self.url = reverse(self.urlconf, kwargs={'pk': self.alert.pk})
        self.login()

    def test_login_required_y_status_code_200(self):
        """Requiere login y estatus code 200 con login."""
        self.client.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

        self.login()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_un_usuario_no_puede_editar_alertas_de_otro_usuario(self):
        """Un usuario no puede ver las alertas de otro cambiando la id en la URI."""
        self.login()
        response = self.client.get(self.urlconf, kwargs={'pk', 2})
        self.assertEqual(response.status_code, 404)

    def test_template(self):
        """Template usado."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'alerts/alerts_form.html')

    def test_subclass(self):
        """Comprueba que sea la subclase del tipo correcto."""
        subclass_alert = forms.BaseAlertForm.get_form_class(self.alert.category)
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], subclass_alert)

    def test_contexto(self):
        """Comprueba el contexto requerido."""
        response = self.client.get(self.url)
        context = response.context

        # Titulo para la pagina
        self.assertEqual(context['title'], 'Editar alerta ')

        # Nombre del buttom type submit.
        self.assertEqual(context['btn_form_name'], 'Actualizar')

        # Nombre de la categoría.
        choices_values = {k: v for k, v in AlertAnuncio.CATEGORY_CHOICES}
        self.assertEqual(
            context['category_name'],
            choices_values[self.alert.category]
        )

    def test_actualiza_alerta(self):
        """Crea una alerta y redirecciona."""
        response = self.client.get(self.url)
        form_data = response.context['form'].initial
        initial_precio = form_data['precio']
        form_data['precio'] = '99999'

        # Polygon es un objeto Polygon, se ha de pasar a string
        form_data['polygon'] = str(form_data['polygon'])

        response = self.client.post(self.url, data=form_data, follow=True)

        # Redirecciona a details
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response=response,
            expected_url=reverse('alerts:details', kwargs={'pk': self.alert.pk}),
            status_code=302,
            target_status_code=200
        )

        # Se ha actualizado el precio
        response = self.client.get(self.url)
        form_data = response.context['form'].initial
        self.assertNotEqual(initial_precio, form_data['precio'])
