from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.utils import timezone
from django.views.generic import TemplateView

from alerts.models import AlertAnuncio
from anuncios.models import Anuncio
from authentication.models import RegisterUser
from blog.models import Article, Tag
from payments.models import PaymentIpn
from pmessages.models import Message
from utils.mixins.views import SuperuserRequiredMixin

UserModel = get_user_model()


class AdminIndexView(SuperuserRequiredMixin, TemplateView):
    """Pagina principal de la administración secundaria."""
    template_name = 'stats/index.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.now = timezone.now()
        self.today = self.now.today()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Usuarios.
        context['total_usuarios'] = UserModel.objects.count()
        context['usuarios_hoy'] = self._usuarios_hoy()
        context['registros_temporales'] = RegisterUser.objects.count()

        # Payments
        context['total_payment'] = PaymentIpn.objects.all().aggregate(Sum('receiver_amount'))
        context['total_payment_week'] = self.get_sum_total_payments(7)
        context['total_payment_month'] = self.get_sum_total_payments(30)

        # Private messages.
        context['pmessages_creados'] = Message.objects.count()

        # Alerts.
        context['alertas_creadas'] = AlertAnuncio.objects.count()

        # Anuncios.
        context['total_anuncios'] = Anuncio.objects.count()
        context['anuncios_activos'] = Anuncio.objects.published().count()
        context['anuncios_ultima_semana'] = self._anuncios_ultima_semana()
        context['anuncios_hoy'] = self._anuncios_hoy()
        context['views_all_anuncios'] = Anuncio.objects.all().aggregate(Sum('views'))

        # Blog
        context['total_tags'] = Tag.objects.count()
        context['total_articles'] = Article.objects.count()

        return context

    def _usuarios_hoy(self):
        """Obtener numero de registros de usuarios hoy."""
        return UserModel.objects.filter(date_joined__date=self.today).count()

    def get_sum_total_payments(self, days):
        """Obtener total ganado en los últimos 'days'."""
        from_datetime = self.now - timezone.timedelta(days=days)
        return PaymentIpn.objects.filter(
            payment_date__gte=from_datetime
        ).aggregate(Sum('receiver_amount'))

    def _anuncios_ultima_semana(self):
        """Obtener numero de anuncios en los últimos 7 días."""
        from_datetime = self.now - timezone.timedelta(days=7)
        return Anuncio.objects.filter(create_at__gte=from_datetime).count()

    def _anuncios_hoy(self):
        """Obtiene el numero de anuncios que se han puesto hoy."""
        return Anuncio.objects.filter(create_at__date=self.today).count()
