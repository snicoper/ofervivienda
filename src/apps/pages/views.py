from django.contrib.sites.models import Site
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.views.generic import TemplateView


class PageMixin(object):
    """Mixin para pages.

    Variables de clase:
    * template_name: Template .html (requerido)
    * template_md: Template .md (no requerido)
    * context_md: Contexto para templates *.md

    Requiere una URLConf para cada vista.

    Si no tiene valor template_md, simplemente renderiza la pagina .html.

    get_context_md similar a get_context_data pero para template_md.
    """
    template_md = None
    context_md = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.template_md:
            try:
                context['template_md'] = get_template(self.template_md).render(
                    self.get_context_md()
                )
            except TemplateDoesNotExist:
                raise TemplateDoesNotExist('Template {} no existe'.format(self.template_md))
        return context

    def get_context_md(self):
        """Similar a get_context_data pero para el *.md."""
        return self.context_md


class CookieConsentView(PageMixin, TemplateView):
    """Muestra la política de cookies."""
    template_name = 'pages/cookie_consent.html'
    template_md = 'pages/cookie_consent.md'

    def get_context_md(self):
        context = super().get_context_md()
        context['SITE'] = Site.objects.get_current()
        return context
