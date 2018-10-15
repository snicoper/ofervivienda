from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from utils.http import get_full_path
from utils.mail import send_templated_mail


def notify_new_pmessage(request, message):
    """Notifica a un recipient de un nuevo mensaje privado."""
    parent = message.parent if message.parent else message
    enlace_message = get_full_path(
        request,
        'pmessages:thread',
        pk=parent.pk
    )
    subject = 'Te han enviado un mensaje privado'
    from_email = settings.GROUP_EMAILS['NO-REPLY']
    recipients = [message.recipient.email]
    template_text = 'pmessages/emails/notify_new_pmessage.txt'
    context = {
        'site_name': get_current_site(request).name,
        'enlace_message': enlace_message
    }
    send_templated_mail(
        subject=subject,
        from_email=from_email,
        recipients=recipients,
        context=context,
        template_text=template_text
    )
