import json
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.crypto import get_random_string
from django.utils.timezone import now

import requests

from utils.http import get_full_path
from utils.mail import send_templated_mail

from .models import PaymentIpn

UserModel = get_user_model()


def generate_invoice():
    """Genera un string único como identificador."""
    while True:
        invoice = get_random_string(length=30)
        if not PaymentIpn.objects.filter(invoice=invoice):
            return invoice


def process_notify_from_paypal(request):
    """Retornar request.POST con _notify-validate.

    Utiliza requests para mandar los datos obtenidos del form.

    Args:
        request (HttpRequest): request de Django.

    Returns:
        True en caso de éxito, False en caso contrario.
    """
    is_valid = True
    errors = []
    params = dict(request.POST.copy())
    params['cmd'] = '_notify-validate'
    response = requests.post(settings.PAYPAL_FORM_ACTION, params=params)
    if not response.status_code == requests.codes.ok:
        is_valid = False
        errors.append(
            'status_code esperaba 200 y es {}'.format(response.status_code)
        )
    if not response.text == 'VERIFIED':
        is_valid = False
        errors.append(
            'response.text esperaba VERIFIED y es {}'.format(response.text)
        )
    if not request.POST.get('payment_status') == 'Completed':
        is_valid = False
        errors.append(
            'payment_status esperaba Completed y es {}'.format(request.POST.get('payment_status'))
        )
    if not request.POST.get('receiver_email') == settings.PAYPAL_RECEIVER_EMAIL:
        is_valid = False
        errors.append(
            'receiver_email no coincide con el esperado'
        )
    if not is_valid:
        write_log_errors(errors)
    return is_valid


def save_data(request):
    """Guarda los datos en al db.

    Solo guarda items en caso de que txn_id no exista en la db y que el
    payment_status sea Completed.

    Desde el campo custom, obtenemos el pk del usuario.

    Args:
        request (HttpRequest): Objeto HttpRequest de la view.

    Returns:
        PaymentIpn: En caso de exito, None en caso contrario.
    """
    post_data = request.POST
    payment_ipn = PaymentIpn.objects.filter(txn_id=post_data.get('txn_id'))
    if not payment_ipn and post_data.get('payment_status') == 'Completed':
        return PaymentIpn.objects.create(
            user=UserModel.objects.get(pk=post_data.get('custom')),
            item_name=post_data.get('item_name'),
            item_number=post_data.get('item_number'),
            invoice=post_data.get('invoice'),
            txn_id=post_data.get('txn_id'),
            total_amount=float(post_data.get('mc_gross')),
            receiver_amount=float(post_data.get('mc_gross')) - float(post_data.get('mc_fee')),
            payment_status=post_data.get('payment_status'),
            post_data=json.dumps(post_data, indent=2)
        )
    return None


def process_account_premium(payment_ipn):
    """Procesa los datos para el usuario.

    Args:
        payment_ipn (PaymentIpn): PaymentIpn asociado a la transacción.

    Returns:
        User: El usuario con el nuevo estado, False en caso de fallo.
    """
    switch = {
        'PREMIUM1': 1,
        'PREMIUM3': 3,
        'PREMIUM6': 6,
        'PREMIUM12': 12
    }
    months = int(switch.get(payment_ipn.item_number, 0))
    if months > 0:
        payment_ipn.user.update_premium(months)
        payment_ipn.user.save()
        return payment_ipn.user
    return False


def process_anuncio_premium(payment_ipn):
    """Incrementa en 1 los anuncios Premium del usuario.

    Args:
        payment_ipn (PaymentIpn): PaymentIpn asociado a la transacción.

    Returns:
        User: El usuario con el nuevo estado.
    """
    payment_ipn.user.increase_anuncio()
    payment_ipn.user.save()
    return payment_ipn.user


def notify_mail_account_premium(request, payment_ipn):
    """Notifica por email que el proceso se ha completado."""
    current_site = get_current_site(request)
    subject = 'Confirmación de premium en {}'.format(current_site.name)
    from_email = settings.GROUP_EMAILS['NO-REPLY']
    recipients = [payment_ipn.user.email]
    template_text = 'payments/mails/notify_premium.txt'
    context = {
        'profile_url': get_full_path(request, 'accounts:profile'),
        'site_name': current_site.name,
        'payment': payment_ipn
    }
    send_templated_mail(
        subject=subject,
        from_email=from_email,
        recipients=recipients,
        context=context,
        template_text=template_text
    )


def notify_mail_anuncio_premium(request, payment_ipn):
    """Notifica por email que el proceso se ha completado."""
    return notify_mail_account_premium(request, payment_ipn)


def write_log_errors(errors):
    """Escribe en un archivo los errores producidos.

    Args:
        errors (list): Lista con los errores a escribir.
    """
    base_root = os.path.dirname(settings.BASE_DIR)
    log_dir = os.path.join(base_root, 'logs')
    filepath = '{}/paypal.log'.format(log_dir)
    error_string = '\n{} : {}'.format(now(), ' : '.join(errors))
    with open(filepath, 'a') as f:
        f.write(error_string)
