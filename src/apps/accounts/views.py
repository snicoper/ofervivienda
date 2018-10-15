from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.geos import GEOSGeometry
from django.urls import reverse
from django.views.generic import (
    DeleteView, DetailView, TemplateView, UpdateView,
)

from pmessages.forms import MessageCreateForm

from .forms import (
    UserLocationUpdateForm, UserOptionsForm, UserProfileUpdateForm,
    UserUpdateAvatarForm,
)
from .models import User, UserLocation, UserOptions


class UserProfileView(LoginRequiredMixin, TemplateView):
    """Perfil privado de usuario.

    Al requerir LoginRequiredMixin y en el template usa 'user.', no prueba nada
    ni añade nada en el context.
    """
    template_name = 'accounts/profile.html'


class UserProfilePublicView(DetailView):
    """Perfil público de usuario.

    Usa User.slug para determinar el usuario a ver.
    """
    template_name = 'accounts/profile_public.html'
    context_object_name = 'profile'
    model = User

    def get_context_data(self, **kwargs):
        """Añade el formulario de contacto."""
        context = super().get_context_data(**kwargs)
        form = MessageCreateForm(self.request.POST or None)
        form.initial['sender'] = self.request.user
        form.initial['recipient'] = self.get_object()
        context['form'] = form
        return context


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Actualiza perfil de usuario."""
    template_name = 'accounts/profile_update.html'
    form_class = UserProfileUpdateForm
    model = User

    def get_object(self, queryset=None):
        """Obtener usuario actual."""
        return self.request.user

    def get_success_url(self):
        msg_success = 'Se ha actualizado los datos del perfil'
        messages.success(self.request, msg_success)
        return super().get_success_url()


class UserAvatarUpdateView(LoginRequiredMixin, UpdateView):
    """Añadir/Actualizar avatar de usuario."""
    template_name = 'accounts/avatar_update.html'
    form_class = UserUpdateAvatarForm
    model = User

    def get_object(self, queryset=None):
        """Obtener usuario actual."""
        return self.request.user

    def get_form(self, form_class=None):
        """Ocultar campo delete_avatar si el usuario no tiene avatar."""
        form = super().get_form(form_class)
        if not self.request.user.avatar:
            form.fields['delete_avatar'].widget = forms.HiddenInput()
        return form

    def form_valid(self, form):
        """Resetear avatar si pulsa marca delete_avatar.

        Si el usuario ha pulsado en delete_avatar, el campo avatar
        se pondrá en '', por lo que restablecerá el valor por defecto.
        """
        if form.cleaned_data['delete_avatar']:
            instance = form.save(commit=False)
            instance.avatar = ''
        return super().form_valid(form)

    def get_success_url(self):
        msg_success = 'Se ha actualizado el avatar'
        messages.success(self.request, msg_success)
        return reverse('accounts:profile')


class UserOptionsDetailView(LoginRequiredMixin, DeleteView):
    """Detalles opciones de usuario."""
    template_name = 'accounts/profile_options.html'
    context_object_name = 'options'
    model = UserOptions

    def get_object(self, queryset=None):
        return self.request.user.user_options


class UserOptionsUpdateView(LoginRequiredMixin, UpdateView):
    """Actualiza opciones de usuario."""
    template_name = 'accounts/options_update.html'
    form_class = UserOptionsForm
    model = UserOptions

    def get_object(self, queryset=None):
        """Obtener options del usuario actual."""
        return self.request.user.user_options

    def get_success_url(self):
        msg_success = 'Se han actualizado las opciones'
        messages.success(self.request, msg_success)
        return reverse('accounts:options')


class UserLocationDetailView(LoginRequiredMixin, DetailView):
    """Mostrar localización del usuario."""
    template_name = 'accounts/profile_location.html'
    context_object_name = 'location'
    model = UserLocation

    def get_object(self, queryset=None):
        return self.request.user.user_location


class UserLocationUpdateView(LoginRequiredMixin, UpdateView):
    """Actualizar localización del usuario."""
    template_name = 'accounts/location_update.html'
    form_class = UserLocationUpdateForm
    model = UserLocation

    def get_object(self, queryset=None):
        """Obtener la localización del usuario actual."""
        return self.request.user.user_location

    def form_valid(self, form):
        latitude = form.cleaned_data['latitude']
        longitude = form.cleaned_data['longitude']
        point = 'POINT({} {})'.format(longitude, latitude)
        instance = form.save(commit=False)
        instance.point = GEOSGeometry(point)
        return super().form_valid(form)

    def get_success_url(self):
        msg_success = 'Se ha actualizado la localización'
        messages.success(self.request, msg_success)
        return reverse('accounts:location')
