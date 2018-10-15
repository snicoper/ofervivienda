from django.conf import settings
from django.contrib.sites.models import Site

from contact.models import ContactMessage
from pmessages.models import Message


def common_template_vars(request):
    """Contexto comunes en los templates."""
    context = {}

    # Todos los usuarios.
    context['SITE'] = Site.objects.get_current()
    context['HTTP_REFERER'] = request.META.get('HTTP_REFERER', '/')
    context['GMAPS_APIKEY'] = settings.GMAPS_APIKEY
    context['PROTOCOL'] = 'https://' if request.is_secure() else 'http://'

    # addsense en debug.
    if settings.DEBUG and getattr(settings, 'ADSENSE_IMAGES_FAKE', False):
        context['ADSENSE_IMAGES_FAKE'] = settings.ADSENSE_IMAGES_FAKE

    # Usuarios logueados
    if request.user.is_authenticated:
        context['INBOX_COUNT'] = inbox_count(request)

    # Administrador
    if request.user.is_superuser:
        context['CONTACT_MESSAGES_UNREAD'] = contact_messages_unread()
    return context


##################################
# Helpers de common_template_vars
##################################

def inbox_count(request):
    """Obtener el numero de pmessages sin leer."""
    if request.user.is_authenticated:
        return Message.objects.inbox_count_for(request.user)
    return 0


def contact_messages_unread():
    """Numero de mensajes en contact sin leer."""
    return ContactMessage.objects.filter(read=False).count()
