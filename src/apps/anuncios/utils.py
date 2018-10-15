from django.conf import settings
from django.contrib.sites.models import Site
from django.urls import reverse

from accounts.models import User
from utils.mail import send_templated_mail


def notify_precio_anuncio_baja(obj, old_precio):
    """Notifica de una bajada de precio en un anuncio.

    Notifica a los usuarios que tienen el anuncio añadido en favoritos de la
    bajada de precio.

    Args:
        obj (Anuncio): Objeto Anuncio.
        old_precio (Decimal): Precio anterior.
    """
    site = Site.objects.get_current()
    url_anuncio = '{}://{}{}'.format(
        settings.PROTOCOL,
        site.domain,
        reverse('anuncios:details', kwargs={'pk': obj.pk})
    )
    context = {
        'site_name': site.name,
        'anuncio_title': obj.get_title,
        'url_anuncio': url_anuncio,
        'new_precio': obj.precio,
        'old_precio': old_precio,
        'currency': obj.get_currency_display()
    }
    recipients = User.objects.filter(
        user_options__notify_precio_anuncio_baja=True,
        favorites_user__anuncios__pk=obj.pk
    ).values('email')
    recipients = [u['email'] for u in recipients]
    subject = 'Se ha rebajado de precio un anuncio en {}'.format(site.name)
    send_templated_mail(
        subject=subject,
        from_email=settings.GROUP_EMAILS['NO-REPLY'],
        recipients=recipients,
        context=context,
        template_text='anuncios/emails/notify_precio_anuncio_baja.txt'
    )
