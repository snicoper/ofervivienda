from django.conf import settings
from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View

from anuncios.settings import ANUNCIO_MIN_DAYS_UPLOAD_UPDATE_AT
from utils.http import get_http_host

from . import settings as payments_settings, utils as payments_utils
from .forms import PaypalIpnForm
from .models import PaymentIpn


class BaseProcessPaymentIpnView(TemplateView):
    """Vista base para mostrar los tipos de pagos.

    Muestra los pagos que las subclases añadan a initials.

    La subclase, crea un formulario por cada initials que haya.
    A la vez, por cada item en initials, ha de haber un item (dict) en la lista
    card_info con keys, values.

    self.initials.append({
        # mis initials
    })
    self.card_info.append({
        'title': 'mi titulo',
        'body': 'mi body para la card',
        'amount': amount
    })

    El primer elemento luego de card_info pertenecerá al primer elemento de initials.

    Requiere usuario con login.

    Attributes:
        form_class (forms.Form): Form a mostrar.
        choices (dict): Diccionario k, v de CHOICES.
        notify_url (str): campo del form notify_url.
        return_url (str): campo del form return.
        cancel_url (str): campo del form cancel_url.

        # Los campos requeridos en las subclases.
        paypal_notify (str): URLConf asociada para notify_url.
        paypal_return (str): URLConf asociada para return_url.
        paypal_cancel (str): URLConf asociada para cancel_url.
        initials (list): una lista para cada form, Form(initial=list).
        card_info (list): una lista para cada form.
    """
    form_class = PaypalIpnForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = {k: v for k, v in PaymentIpn.PAYMENT_CHOICES}
        self.notify_url = ''
        self.return_url = ''
        self.cancel_url = ''
        self.paypal_notify = ''
        self.paypal_return = ''
        self.paypal_cancel = ''
        self.initials = []
        self.card_info = []

    def dispatch(self, request, *args, **kwargs):
        """Inicializa algunos atributos de clase.

        El usuario ha de estar logueado o lo redireccionara a login.
        """
        if not request.user.is_authenticated:
            redirect_url = '{}?next={}'.format(
                settings.LOGIN_URL,
                request.get_full_path()
            )
            return redirect(redirect_url)
        host = get_http_host(request)
        self.return_url = '{}{}'.format(host, self.paypal_return)
        self.notify_url = '{}{}'.format(host, self.paypal_notify)
        self.cancel_url = '{}{}'.format(host, self.paypal_cancel)
        self.get_initials()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Genera los forms y los pone en contexto."""
        context = super().get_context_data(**kwargs)
        forms = [self.form_class(initial=i) for i in self.initials]
        context['forms'] = forms
        context['form_action'] = settings.PAYPAL_FORM_ACTION
        context['card_info'] = self.card_info
        context['reload_update_at'] = ANUNCIO_MIN_DAYS_UPLOAD_UPDATE_AT
        return context


class ProcessAccountPremiumView(BaseProcessPaymentIpnView):
    """Muestra los precios para account Premium en Cards."""
    template_name = 'payments/process_account_premium.html'

    def __init__(self, *args, **kwargs):
        """Añadir URLConf a los campos que lo requieren."""
        super().__init__(*args, **kwargs)
        self.paypal_notify = reverse('payments:notify_account_premium')
        self.paypal_return = reverse('payments:return_premium')
        self.paypal_cancel = reverse('accounts:profile')

    def get_initials(self):
        """Crea valores por defecto en los forms.

        Cada self.initials que se crea, es un form mas que se mostrara en el template.

        El template se le pasa un lista con diccionarios como elementos con
        self.card_info, cada posición de la lista (cada diccionario) tiene que
        tener la misma posición que el form en self.initials.
        """
        amount = payments_settings.PAYMENTS_PREMIUM1
        self.initials.append({
            'amount': amount,
            'item_name': self.choices.get('PREMIUM1'),
            'item_number': 'PREMIUM1',
            'invoice': payments_utils.generate_invoice(),
            'custom': self.request.user.pk,
            'notify_url': self.notify_url,
            'return': self.return_url,
            'cancel_return': self.cancel_url
        })
        self.card_info.append({
            'title': self.choices.get('PREMIUM1'),
            'body': '',
            'amount': amount
        })
        amount = payments_settings.PAYMENTS_PREMIUM3
        self.initials.append({
            'amount': amount,
            'item_name': self.choices.get('PREMIUM3'),
            'item_number': 'PREMIUM3',
            'invoice': payments_utils.generate_invoice(),
            'custom': self.request.user.pk,
            'notify_url': self.notify_url,
            'return': self.return_url,
            'cancel_return': self.cancel_url
        })
        self.card_info.append({
            'title': self.choices.get('PREMIUM3'),
            'body': '',
            'amount': amount
        })
        amount = payments_settings.PAYMENTS_PREMIUM6
        self.initials.append({
            'amount': amount,
            'item_name': self.choices.get('PREMIUM6'),
            'item_number': 'PREMIUM6',
            'invoice': payments_utils.generate_invoice(),
            'custom': self.request.user.pk,
            'notify_url': self.notify_url,
            'return': self.return_url,
            'cancel_return': self.cancel_url
        })
        self.card_info.append({
            'title': self.choices.get('PREMIUM6'),
            'body': '',
            'amount': amount
        })
        amount = payments_settings.PAYMENTS_PREMIUM12
        self.initials.append({
            'amount': amount,
            'item_name': self.choices.get('PREMIUM12'),
            'item_number': 'PREMIUM12',
            'invoice': payments_utils.generate_invoice(),
            'custom': self.request.user.pk,
            'notify_url': self.notify_url,
            'return': self.return_url,
            'cancel_return': self.cancel_url
        })
        self.card_info.append({
            'title': self.choices.get('PREMIUM12'),
            'body': '',
            'amount': amount
        })


class ProcessAnuncioPremiumView(BaseProcessPaymentIpnView):
    """Muestra el precio para anuncio Premium en Card."""
    template_name = 'payments/process_anuncio_premium.html'

    def __init__(self, *args, **kwargs):
        """Añadir URLConf a los campos que lo requieren."""
        super().__init__(*args, **kwargs)
        self.paypal_notify = reverse('payments:notify_anuncio_premium')
        self.paypal_return = reverse('payments:return_premium')
        self.paypal_cancel = reverse('accounts:profile')

    def get_initials(self):
        """Crea valores por defecto en los forms.

        @see: ProcessAccountPremiumView.get_initials()
        """
        amount = payments_settings.PAYMENTS_ANUNCIO
        self.initials.append({
            'amount': amount,
            'item_name': self.choices.get('ANUNCIO'),
            'item_number': 'ANUNCIO',
            'invoice': payments_utils.generate_invoice(),
            'custom': self.request.user.pk,
            'notify_url': self.notify_url,
            'return': self.return_url,
            'cancel_return': self.cancel_url
        })
        self.card_info.append({
            'title': self.choices.get('ANUNCIO'),
            'body': '',
            'amount': amount
        })


@method_decorator(csrf_exempt, name='dispatch')
class BaseNotifyView(View):
    """Notificación del IPN de PayPal.

    BaseNotifyView comprueba y procesa la parte de validación y guarda el objeto
    si la validación es correcta.
    La subclases, son las encargadas de hacer el resto.

    Attributes:
        payment_ipn (PaymentIpn): Objeto guardado en caso de éxito en la validación.
    """
    payment_ipn = None

    def dispatch(self, request, *args, **kwargs):
        """Si HTTP es POST, hace la verificación de la transacción."""
        if request.method == 'POST':
            is_valid = payments_utils.process_notify_from_paypal(request)
            if is_valid:
                self.payment_ipn = payments_utils.save_data(request)
            else:
                return HttpResponse('BAD')
        else:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)


class NotifyAccountPremiumView(BaseNotifyView):
    """Notificado cuando hace un pago de cuenta Premium."""

    def post(self, request, *args, **kwargs):
        """Procesa y manda una notificación por email.

        Añade al usuario como is_premium = True y añade el tiempo de expiración
        en el campo expire_premium_at del usuario.

        Notifica por mail que el proceso se ha completado y ya es un usuario
        premium (o a añadido tiempo).
        """
        if request.POST.get('payment_status') == 'Completed':
            payments_utils.process_account_premium(self.payment_ipn)
            payments_utils.notify_mail_account_premium(request, self.payment_ipn)
        return HttpResponse('OKAY')


class NotifyAnuncioPremiumView(BaseNotifyView):
    """Notificado cuando hace un pago de un anuncio Premium."""

    def post(self, request, *args, **kwargs):
        """Incrementa en uno los anuncios Premium del usuario."""
        if request.POST.get('payment_status') == 'Completed':
            payments_utils.process_anuncio_premium(self.payment_ipn)
            payments_utils.notify_mail_anuncio_premium(request, self.payment_ipn)
        return HttpResponse('OKAY')


@method_decorator(csrf_exempt, name='dispatch')
class ReturnView(TemplateView):
    """Base para vistas returns."""
    template_name = 'payments/return.html'

    def dispatch(self, request, *args, **kwargs):
        """Http GET o Http POST sin datos redirecciona."""
        if request.method != 'POST' or not request.POST:
            return redirect('/')
        return render(request, self.template_name)
