import os

from django.urls import reverse

from gallery import settings as images_settings
from tests.unit.images import simple_uploaded_file

from .base_gallery import BaseGalleryTest


class ImageAnuncioListViewTest(BaseGalleryTest):

    def setUp(self):
        super().setUp()
        # Anuncio pk 14 tiene imágenes.
        self.anuncio = self.anuncio_model.objects.get(pk=14)
        self.url = 'gallery:anuncio_gallery_list'
        self.urlconf = reverse(self.url, kwargs={'id_anuncio': self.anuncio.pk})
        self.login()
        self.response = self.client.get(self.urlconf)

    def test_status_code_owner_anuncio(self):
        """Al owner del anuncio, le mostrara la galería."""
        self.assertEqual(self.response.status_code, 200)

    def test_usuario_login_no_owner_anuncio(self):
        """Un usuario logueado que intenta ver la galería de otro usuario, sera
        redireccionado a Http404.
        """
        self.logout()
        self.login('perico', '123')
        response = self.client.get(self.urlconf)

        self.assertEqual(response.status_code, 404)

    def test_usuario_anonimo_status_code_404(self):
        """Al usuario anónimo, lo redirecciona a pagina de login."""
        self.logout()
        response = self.client.get(self.urlconf, follow=True)
        expected_url = '{}?next={}'.format(
            reverse('authentication:login'),
            self.urlconf
        )

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

    def test_template_usado(self):
        """Prueba el template usado."""
        self.assertTemplateUsed(self.response, 'gallery/gallery_list.html')

    def test_context_data(self):
        """Prueba el get_context_data."""
        self.assertIn('anuncio', self.response.context)

    def test_queryset(self):
        """Mostrara solo las imágenes que pertenece al anuncio."""
        # Es necesario añadir una imagen en otro anuncio.
        image_path = os.path.join(os.path.dirname(__file__), 'image.jpg')
        image_obj = self.image_model()
        image_obj.anuncio = self.anuncio_model.objects.get(pk=1)
        image_obj.image = simple_uploaded_file(image_path)
        image_obj.save()

        # Total de imágenes 8, 7 de fixtures y el creado.
        self.assertEqual(self.image_model.objects.count(), 8)

        # El anuncio tiene 7 imágenes.
        self.assertEqual(self.response.context['image_list'].count(), 7)

        image_obj.delete()


class ImageAnuncioCreateViewTest(BaseGalleryTest):

    def setUp(self):
        super().setUp()
        self.anuncio = self.anuncio_model.objects.get(pk=1)
        self.url = 'gallery:image_anuncio_add'
        self.urlconf = reverse(self.url, kwargs={'id_anuncio': self.anuncio.pk})
        self.login()
        self.response = self.client.get(self.urlconf)

    def tearDown(self):
        """Eliminar anuncio por si se le a añadido imágenes, que las elimine del
        disco.
        """
        self.anuncio.delete()

    def test_status_code_owner_anuncio(self):
        """Al owner del anuncio, le mostrara la galería."""
        self.assertEqual(self.response.status_code, 200)

    def test_usuario_login_no_owner_anuncio(self):
        """Un usuario logueado que intenta ver la galería de otro usuario, sera
        redireccionado a Http404.
        """
        self.logout()
        self.login('perico', '123')
        response = self.client.get(self.urlconf)

        self.assertEqual(response.status_code, 404)

    def test_usuario_anonimo_status_code_404(self):
        """Al usuario anónimo, lo redirecciona a pagina de login."""
        self.logout()
        response = self.client.get(self.urlconf, follow=True)
        expected_url = '{}?next={}'.format(
            reverse('authentication:login'),
            self.urlconf
        )

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

    def test_template_usado(self):
        """Prueba el template usado."""
        self.assertTemplateUsed(self.response, 'gallery/images_add.html')

    def test_maximo_imagenes(self):
        """Si tiene mas imágenes, redireccionara a la pagina de pago."""
        anuncio = self.anuncio_model.objects.get(pk=14)
        urlconf = reverse(self.url, kwargs={'id_anuncio': anuncio.pk})
        response = self.client.get(urlconf)
        expected_url = reverse('payments:process_anuncio_premium')

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

    def test_context_data(self):
        """Prueba el context data."""
        context = self.response.context

        # formset
        self.assertIn('formset', context)

        # images_max, Máximo de imágenes que aun puede subir.
        self.assertIn('images_max', context)

        # El total ha de ser de IMAGES_MAX_IMAGES
        self.assertEqual(context['images_max'], images_settings.IMAGES_MAX_IMAGES)

        # anuncio en context.
        self.assertIn('anuncio', context)
        self.assertEqual(context['anuncio'].pk, 1)

        # Si el anuncio no es premium, context['restantes'] existirá.
        self.assertIn('restantes', context)
        self.assertEqual(context['restantes'], 5)

        # El anuncio es premium, no existirá context['restantes']
        self.anuncio.is_premium = True
        self.anuncio.save()
        response = self.client.get(self.urlconf)

        self.assertNotIn('restantes', response.context)

    def test_get_form(self):
        """Si el anuncio no es premium y no tiene imágenes, formset tendrá 5
        imágenes para poner.

        Si mas tarde se añade 1 imagen, solo mostrara 4.
        """
        # Añadir una imagen al anuncio.
        image_path = os.path.join(os.path.dirname(__file__), 'image.jpg')
        image_obj = self.image_model()
        image_obj.anuncio = self.anuncio_model.objects.get(pk=1)
        image_obj.image = simple_uploaded_file(image_path)
        image_obj.save()
        response = self.client.get(self.urlconf)
        formset = response.context['formset']

        # formset tiene 4 elementos
        self.assertEqual(len(formset), 4)

    def test_post_anuncio_normal(self):
        """Envía dos imágenes en un anuncio."""
        image_path = os.path.join(os.path.dirname(__file__), 'image.jpg')
        form_data = {
            'management_form': self.response.context['formset'].management_form,
            'form-TOTAL_FORMS': '5',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '5',
            'form-0-image': simple_uploaded_file(image_path),
            'form-1-image': simple_uploaded_file(image_path),
            'form-2-image': '',
            'form-3-image': '',
            'form-4-image': '',
            'form-0-description': '',
            'form-1-description': '',
            'form-2-description': '',
            'form-3-description': '',
            'form-4-description': '',
        }
        response = self.client.post(self.urlconf, data=form_data)
        expected_url = reverse(
            'gallery:anuncio_gallery_list',
            kwargs={'id_anuncio': self.anuncio.pk}
        )

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

        # Ahora, mostrara solo 3 forms.
        """Envía dos imágenes en un anuncio."""
        form_data = {
            'management_form': self.response.context['formset'].management_form,
            'form-TOTAL_FORMS': '3',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '3',
            'form-0-image': simple_uploaded_file(image_path),
            'form-1-image': simple_uploaded_file(image_path),
            'form-2-image': ''
        }
        response = self.client.post(self.urlconf, data=form_data)
        expected_url = reverse(
            'gallery:anuncio_gallery_list',
            kwargs={'id_anuncio': self.anuncio.pk}
        )

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

    def test_post_anuncio_premium(self):
        """Envía dos imágenes en un anuncio."""
        self.anuncio.is_premium = True
        self.anuncio.save()
        image_path = os.path.join(os.path.dirname(__file__), 'image.jpg')
        form_data = {
            'management_form': self.response.context['formset'].management_form,
            'form-TOTAL_FORMS': '5',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '5',
            'form-0-image': simple_uploaded_file(image_path),
            'form-1-image': simple_uploaded_file(image_path),
            'form-2-image': '',
            'form-3-image': '',
            'form-4-image': '',
        }
        response = self.client.post(self.urlconf, data=form_data)
        expected_url = reverse(
            'gallery:anuncio_gallery_list',
            kwargs={'id_anuncio': self.anuncio.pk}
        )

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

        # Ahora, mostrara solo 3 forms.
        """Envía dos imágenes en un anuncio."""
        form_data = {
            'management_form': self.response.context['formset'].management_form,
            'form-TOTAL_FORMS': '5',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '5',
            'form-0-image': simple_uploaded_file(image_path),
            'form-1-image': simple_uploaded_file(image_path),
            'form-2-image': simple_uploaded_file(image_path),
            'form-3-image': simple_uploaded_file(image_path),
            'form-4-image': simple_uploaded_file(image_path),
        }
        response = self.client.post(self.urlconf, data=form_data)
        expected_url = reverse(
            'gallery:anuncio_gallery_list',
            kwargs={'id_anuncio': self.anuncio.pk}
        )

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )


class ImageAnuncioUpdateViewTest(BaseGalleryTest):

    def setUp(self):
        super().setUp()
        self.image_path = os.path.join(os.path.dirname(__file__), 'image.jpg')
        self.anuncio = self.anuncio_model.objects.get(pk=1)
        self.image = self.image_model()
        self.image.anuncio = self.anuncio
        self.image.image = simple_uploaded_file(self.image_path)
        self.image.save()
        self.url = 'gallery:image_anuncio_update'
        self.urlconf = reverse(self.url, kwargs={'pk': self.image.pk})
        self.login()
        self.response = self.client.get(self.urlconf)

    def test_status_code_owner_anuncio(self):
        """Al owner del anuncio, le mostrara la galería."""
        self.assertEqual(self.response.status_code, 200)

    def test_usuario_login_no_owner_anuncio(self):
        """Un usuario logueado que intenta ver la galería de otro usuario, sera
        redireccionado a Http404.
        """
        self.logout()
        self.login('perico', '123')
        response = self.client.get(self.urlconf)

        self.assertEqual(response.status_code, 404)

    def test_usuario_anonimo_status_code_404(self):
        """Al usuario anónimo, lo redirecciona a pagina de login."""
        self.logout()
        response = self.client.get(self.urlconf, follow=True)
        expected_url = '{}?next={}'.format(
            reverse('authentication:login'),
            self.urlconf
        )

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

    def test_template_usado(self):
        """Prueba el template usado."""
        self.assertTemplateUsed(self.response, 'gallery/image_update.html')

    def test_post(self):
        image_path = os.path.join(os.path.dirname(__file__), 'image.jpg')
        form_data = {
            'image': simple_uploaded_file(image_path),
            'anuncio': self.anuncio.pk
        }
        old_image = self.image.image.name
        response = self.client.post(self.urlconf, data=form_data, follow=True)
        expected_url = reverse(
            'gallery:anuncio_gallery_list',
            kwargs={'id_anuncio': self.anuncio.pk}
        )

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

        # El nombre de la imagen a cambiado.
        image = self.image_model.objects.get(pk=1)
        self.assertNotEqual(old_image, image.image.name)


class ImageAnuncioDeleteViewTest(BaseGalleryTest):

    def setUp(self):
        super().setUp()
        self.image_path = os.path.join(os.path.dirname(__file__), 'image.jpg')
        self.anuncio = self.anuncio_model.objects.get(pk=1)
        self.image_obj = self.image_model()
        self.image_obj.anuncio = self.anuncio
        self.image_obj.image = simple_uploaded_file(self.image_path)
        self.image_obj.save()
        self.url = 'gallery:image_anuncio_delete'
        self.urlconf = reverse(self.url, kwargs={'pk': self.image_obj.pk})
        self.login()
        self.response = self.client.get(self.urlconf)

    def tearDown(self):
        """Eliminar anuncio para asegurarse que elimina las imágenes en disco."""
        self.image_obj.delete()

    def test_status_code_owner_anuncio(self):
        """Al owner del anuncio, le mostrara la galería."""
        self.assertEqual(self.response.status_code, 200)

    def test_usuario_login_no_owner_anuncio(self):
        """Un usuario logueado que intenta ver la galería de otro usuario, sera
        redireccionado a Http404.
        """
        self.logout()
        self.login('perico', '123')
        response = self.client.get(self.urlconf)

        self.assertEqual(response.status_code, 404)

    def test_usuario_anonimo_status_code_404(self):
        """Al usuario anónimo, lo redirecciona a pagina de login."""
        self.logout()
        response = self.client.get(self.urlconf, follow=True)
        expected_url = '{}?next={}'.format(
            reverse('authentication:login'),
            self.urlconf
        )

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

    def test_template_usado(self):
        """Prueba el template usado."""
        self.assertTemplateUsed(self.response, 'gallery/delete_confirm.html')

    def test_post_elimina_imagen(self):
        """Elimina una imagen del la db y del disco."""
        image_id = self.image_obj.pk
        image_path = self.image_obj.image.path
        response = self.client.post(self.urlconf)
        expected_url = reverse(
            'gallery:anuncio_gallery_list',
            kwargs={'id_anuncio': self.anuncio.pk}
        )

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

        # La imagen ya no existe en la db.
        self.assertFalse(self.image_model.objects.filter(pk=image_id))

        # También se ha eliminado del disco.
        self.assertFalse(os.path.exists(image_path))
