from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from . import settings as images_settings
from .forms import ImageAnuncioCreateForm, ImageAnuncioForm
from .mixins.views import (
    CheckIsOwnerByAnuncioIdMixin, CheckIsOwnerByImageIdMixin,
)
from .models import ImageAnuncio


class ImageAnuncioListView(LoginRequiredMixin, CheckIsOwnerByAnuncioIdMixin, ListView):
    """Muestra la galería de imágenes de un anuncio."""
    template_name = 'gallery/gallery_list.html'
    context_object_name = 'image_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['anuncio'] = self.anuncio
        return context

    def get_queryset(self):
        """Obtener las imágenes de un anuncios con id_anuncio."""
        return ImageAnuncio.objects.filter(anuncio=self.kwargs.get('id_anuncio'))


class ImageAnuncioCreateView(LoginRequiredMixin, CheckIsOwnerByAnuncioIdMixin, CreateView):
    """Añadir una imagen a un anuncio.

    stackoverflow.com/questions/34006994/how-to-upload-multiple-images-to-a-blog-post-in-django
    """
    template_name = 'gallery/images_add.html'
    model = ImageAnuncio

    def get(self, request, *args, **kwargs):
        """Si no es un anuncio premium o ha llegado al limite de imágenes en el
        anuncio, redireccionara para poder pagar un anuncio y convertir el
        anuncio a Premium.
        """
        images_anuncio_count = self.anuncio.image_anuncio.count()
        if self.anuncio.is_premium or images_anuncio_count < images_settings.IMAGES_MAX_IMAGES:
            return super().get(request, *args, **kwargs)
        msg_warning = 'Has llegado al limite de imágenes'
        messages.warning(request, msg_warning)
        return redirect(reverse('payments:process_anuncio_premium'))

    def post(self, request, *args, **kwargs):
        """Los forms con el campo image vacío, los ignora."""
        formset = self.get_form()
        for form in formset.cleaned_data:
            image = form.get('image')
            if image:
                instance = ImageAnuncio()
                instance.image = image
                instance.description = form.get('description') or ''
                instance.anuncio = self.anuncio
                instance.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        """Añade el formset en el contexto."""
        context = super().get_context_data(**kwargs)
        context['formset'] = self.get_form()
        context['anuncio'] = self.anuncio

        # Avisa de las imágenes que puede poner si no es un anuncio Premium.
        if not self.anuncio.is_premium:
            context['restantes'] = (
                images_settings.IMAGES_MAX_IMAGES - self.anuncio.image_anuncio.count()
            )
            context['images_max'] = images_settings.IMAGES_MAX_IMAGES
        return context

    def get_form(self, form_class=None):
        """Obtener el formset.

        Si no es un anuncio premium, mostrara un maximo de IMAGES_MAX_IMAGES
        menos las imágenes que tenga ya puestas.

        Si es un anuncio premium, las mostrara siempre con un form de 5 items.
        """
        extra = images_settings.IMAGES_MAX_IMAGES
        if not self.anuncio.is_premium:
            extra = images_settings.IMAGES_MAX_IMAGES - self.anuncio.image_anuncio.count()
        ImageAnuncioFormSet = modelformset_factory(
            ImageAnuncio,
            form=ImageAnuncioCreateForm,
            extra=extra
        )
        return ImageAnuncioFormSet(
            self.request.POST or None,
            self.request.FILES or None,
            queryset=ImageAnuncio.objects.none()
        )

    def get_success_url(self):
        id_anuncio = self.kwargs.get('id_anuncio')
        msg_success = 'Imágenes añadida con éxito.'
        messages.success(self.request, msg_success)
        return reverse('gallery:anuncio_gallery_list', kwargs={'id_anuncio': id_anuncio})


class ImageAnuncioUpdateView(LoginRequiredMixin, CheckIsOwnerByImageIdMixin, UpdateView):
    """Actualiza (cambia) una imagen."""
    template_name = 'gallery/image_update.html'
    context_object_name = 'actual_image'
    form_class = ImageAnuncioForm
    model = ImageAnuncio

    def get_success_url(self):
        msg_success = 'Imagen cambiada con éxito.'
        messages.success(self.request, msg_success)
        return reverse('gallery:anuncio_gallery_list', kwargs={'id_anuncio': self.anuncio.pk})


class ImageAnuncioDeleteView(LoginRequiredMixin, CheckIsOwnerByImageIdMixin, DeleteView):
    """Elimina una imagen."""
    template_name = 'gallery/delete_confirm.html'
    model = ImageAnuncio
    context_object_name = 'image'

    def get_success_url(self):
        """Redirecciona después de eliminar una imagen.

        Redirecciona a la galería de imágenes que pertenece un anuncio.
        """
        msg_success = 'Imagen eliminada con éxito.'
        messages.success(self.request, msg_success)
        return reverse(
            'gallery:anuncio_gallery_list', kwargs={'id_anuncio': self.anuncio.pk}
        )
