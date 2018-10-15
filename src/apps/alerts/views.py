from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import Http404, redirect
from django.urls import reverse
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView,
)

from anuncios.mixins.views import ClassFromCategoryNameMixin, ClassFromIDMixin

from . import forms
from .models import AlertAnuncio


class AlertUserListView(LoginRequiredMixin, ListView):
    """Lista de alertas del usuario."""
    template_name = 'alerts/list.html'
    context_object_name = 'alert_list'
    model = AlertAnuncio

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


class AlertDetailsView(LoginRequiredMixin, ClassFromIDMixin, DetailView):
    template_name = 'alerts/details.html'
    context_object_name = 'alert'
    model = AlertAnuncio

    def dispatch(self, request, *args, **kwargs):
        """Las alertas solo las puede ver el owner."""
        if request.user != self.get_object().owner:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class AlertFormViewMixin(LoginRequiredMixin):
    """Mixin para crear y editar una alerta.

    Las subclases requieren de 3 atributos:
        - msg_seccess (str): Mensaje en caso de éxito.
        - title (str): Titulo, usado para el template.
        - btn_form_name (str): Texto del botón del formulario.
    """
    template_name = 'alerts/alerts_form.html'
    context_object_name = 'alert'
    model = AlertAnuncio

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = {k: v for k, v in AlertAnuncio.CATEGORY_CHOICES}
        context['btn_form_name'] = self.btn_form_name
        context['title'] = self.title
        context['category_name'] = categories.get(self.category, None)

        # Para el css, bgcolor-{{ category_css }}
        context['category_css'] = self.category.lower()
        return context

    def get_form_class(self):
        return forms.BaseAlertForm.get_form_class(self.category)

    def form_valid(self, form):
        messages.success(self.request, self.msg_seccess)
        return super().form_valid(form)


class AlertCreateView(ClassFromCategoryNameMixin, AlertFormViewMixin, CreateView):
    """Crea una nueva alerta."""
    msg_seccess = 'Se a creado una nueva alerta'
    title = 'Añadir nueva alerta '
    btn_form_name = 'Crear'

    def get_initial(self):
        initial = super().get_initial()
        initial['owner'] = self.request.user.pk
        initial['category'] = self.category
        if self.request.user.user_location.latitude:
            initial['latitude'] = self.request.user.user_location.latitude
            initial['longitude'] = self.request.user.user_location.longitude
        return initial


class AlertUpdateView(ClassFromIDMixin, AlertFormViewMixin, UpdateView):
    """Actualizar una alerta."""
    msg_seccess = 'Se a actualizado con éxito la alerta'
    btn_form_name = 'Actualizar'
    title = 'Editar alerta '

    def dispatch(self, request, *args, **kwargs):
        """Comprueba que el usuario es el owner de la alerta."""
        if request.user != self.get_object().owner:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Añadir al contexto la descripción de la alerta."""
        context = super().get_context_data(**kwargs)
        context['description'] = self.get_object().description
        return context


class AlertDeleteView(LoginRequiredMixin, DeleteView):
    """Un usuario elimina una alerta."""
    template_name = 'alerts/delete.html'
    context_object_name = 'alert'
    model = AlertAnuncio

    def dispatch(self, request, *args, **kwargs):
        """Comprueba que el usuario es owner de la alerta."""
        if not request.user.is_authenticated or request.user != self.get_object().owner:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        msg_success = 'Se ha eliminado la alerta'
        messages.success(self.request, msg_success)
        return reverse('alerts:list')


class AlertsAllDeleteView(LoginRequiredMixin, TemplateView):
    """Elimina todas las alertas de un usuario."""
    template_name = 'alerts/delete_all.html'

    def post(self, request, *args, **kwargs):
        if request.POST.get('delete_all'):
            AlertAnuncio.objects.filter(owner=request.user).delete()
            msg_success = 'Se han eliminado todas las alertas'
            messages.success(request, msg_success)
        return redirect(reverse('alerts:list'))
