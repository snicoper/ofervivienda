from django import forms
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import FormView

from anuncios.models import Anuncio
from utils.http import get_full_path
from utils.mail import send_templated_mail

from .forms import RecommendForm


class RecommendAnuncioIndexView(FormView):
    """Muestra el form para recomendar un anuncio."""
    template_name = 'recommend/form.html'
    form_class = RecommendForm
    anuncio = None

    def dispatch(self, request, *args, **kwargs):
        """Comprobar que el anuncio existe."""
        self.anuncio = get_object_or_404(Anuncio, pk=self.kwargs.get('anuncio_id'))
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        """Si es un usuario logueado, obtener el email."""
        form = super().get_form(form_class)
        if self.request.user.is_authenticated:
            form.fields['from_email'].widget = forms.HiddenInput()
            form.initial['from_email'] = self.request.user.email
        return form

    def get_context_data(self, **kwargs):
        """Añadir anuncio al context."""
        context = super().get_context_data(**kwargs)
        context['anuncio'] = self.anuncio
        return context

    def form_valid(self, form):
        """Si el form es valido, enviar el email de recomendación."""
        current_site = get_current_site(self.request)
        recipients = [form.cleaned_data.get('email_to')]
        from_email = form.cleaned_data.get('from_email')
        body = form.cleaned_data.get('body')
        link_anuncio = get_full_path(self.request, 'anuncios:details', pk=self.anuncio.pk)
        context = {
            'from_email': from_email,
            'body': body,
            'link_anuncio': link_anuncio,
            'site_name': current_site.name,
            'site_domain': current_site.domain
        }
        send_templated_mail(
            subject='Recomendación de un anuncio en {}'.format(current_site.name),
            from_email=from_email,
            recipients=recipients,
            context=context,
            template_text='recommend/emails/recommend.txt',
            reply_to=[from_email]
        )
        msg_success = 'Se ha enviado con éxito el mensaje'
        messages.success(self.request, msg_success)
        return redirect(reverse(
            'anuncios:details', kwargs={'pk': self.anuncio.pk}
        ))
