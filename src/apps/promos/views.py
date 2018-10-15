from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, FormView

from payments.models import PaymentIpn
from utils.http import get_full_path
from utils.mail import send_templated_mail
from utils.mixins.views import SuperuserRequiredMixin

from .forms import GenerateCodePromoToUserForm, PromoValidateCodeForm
from .models import Promo
from .settings import PROMO_EXPIRE_DAYS

UserModel = get_user_model()


class GenerateCodePromoView(SuperuserRequiredMixin, CreateView):
    """Genera un código de promoción y lo notifica por email.

    Si solo se quiere crear un código, usar el admin de Django.
    """
    template_name = 'promos/create_code_promo.html'
    form_class = GenerateCodePromoToUserForm
    model = Promo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['promo_expire_days'] = PROMO_EXPIRE_DAYS
        return context

    def get_success_url(self):
        """Si todo ha ido bien, notificar por email al usuario
        y enviar el código generado.
        """
        self._send_notify_mail()
        msg_success = 'Se ha creado y enviado el código'
        messages.success(self.request, msg_success)
        return reverse('promos:generate_code_promo')

    def _send_notify_mail(self):
        code = self.object.code
        user_id = self.request.POST['to_user']
        payment_promo = self.request.POST['payment_promo']
        user = UserModel.objects.get(pk=user_id)
        site = get_current_site(self.request)
        promotion_list = {k: v for k, v in PaymentIpn.PAYMENT_CHOICES}
        context = {
            'code': code,
            'user': user,
            'site_name': site.name,
            'promotion': promotion_list.get(payment_promo),
            'promo_expire_days': self.object.expire_at,
            'link_profile': get_full_path(self.request, 'accounts:profile')
        }
        send_templated_mail(
            subject='Código de promoción en {}'.format(site.name),
            from_email=settings.GROUP_EMAILS['NO-REPLY'],
            recipients=[user.email],
            context=context,
            template_text='promos/emails/send_code.txt'
        )


class PromoValidateCodeView(LoginRequiredMixin, FormView):
    template_name = 'promos/validate_code.html'
    form_class = PromoValidateCodeForm

    def form_valid(self, form):
        """El form se encarga de comprobar si el code existe en la db, que no
        este expirado y que no haya sido utilizado ya, por lo que si llega hasta
        aquí, significa que todo OK.
        """
        code = form.cleaned_data['code']
        promo = Promo.objects.get(code=code)
        promo.active_promo(self.request.user)
        promo.save()
        msg_success = 'Se ha añadido el código de promoción con éxito'
        messages.success(self.request, msg_success)
        return redirect(reverse('accounts:profile'))
