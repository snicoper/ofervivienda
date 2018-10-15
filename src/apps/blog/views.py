from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db.models import Count, F
from django.shortcuts import Http404, get_object_or_404, redirect
from django.template.loader import get_template
from django.views.generic import (
    DetailView, FormView, ListView, MonthArchiveView, TemplateView, View,
    YearArchiveView,
)

from .forms import ArticleRecommendForm
from .models import Article, ArticleSubscribe, Tag


class ArticleListView(ListView):
    """Muestra lista de artículos."""
    template_name = 'blog/article_list.html'
    context_object_name = 'article_list'
    model = Article
    paginate_by = 12

    def get_queryset(self):
        if self.queryset is not None:
            queryset = self.queryset.published()
        else:
            queryset = self.model.objects.published()
        return queryset.select_related(
            'owner',
            'default_tag'
        ).prefetch_related('tags')


class ArticleDetailView(DetailView):
    """Detalles del articulo."""
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'
    model = Article

    def dispatch(self, request, *args, **kwargs):
        self.model.objects.filter(slug=kwargs.get('slug')).update(views=F('views') + 1)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().select_related('owner')


class TagListView(ListView):
    """Muestra lista de etiquetas."""
    template_name = 'blog/tag_list.html'
    context_object_name = 'tag_list'
    model = Tag

    def get_queryset(self):
        """Añade la propiedad articles_count, con la cantidad de
        articulos en cada Tag.
        """
        return super().get_queryset().annotate(
            articles_count=Count('article_tags')
        )


class ArticleListByTagNameListView(ArticleListView):
    """Muestra artículos de una categoría."""

    def dispatch(self, request, *args, **kwargs):
        """Incrementa +1 'Tag.views'."""
        slug = self.kwargs.get('slug')
        get_object_or_404(Tag, slug=slug)
        self.model.objects.filter(slug=slug).update(views=F('views') + 1)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Obtener lista de articulos por tag categoria."""
        return super().get_queryset().filter(tags__slug=self.kwargs.get('slug'))


class ArticleRecommendView(FormView):
    """Recomienda un articulo por email a una persona."""
    form_class = ArticleRecommendForm
    template_name = 'blog/article_recommend.html'

    def get_context_data(self, **kwargs):
        article = get_object_or_404(Article, slug=self.kwargs.get('slug'))
        context = super().get_context_data(**kwargs)
        context['article'] = article
        return context

    def form_valid(self, form):
        article = get_object_or_404(Article, slug=self.kwargs.get('slug'))
        messages.success(self.request, 'Se ha enviado el mensaje correctamente.')
        cdata = form.cleaned_data
        context = {
            'article': article,
            'name': cdata['name'],
            'message': cdata['message'],
            'site': get_current_site(self.request)
        }
        template_email = get_template('blog/emails/article_recommend.txt').render(context)
        send_mail(
            subject='{} te recomienda que leas un articulo'.format(cdata['name']),
            message=template_email,
            from_email=cdata['from_email'],
            recipient_list=[cdata['to_email']]
        )
        return redirect(article.get_absolute_url())


class ArticleArchiveIndexView(TemplateView):
    """Mostrar por años y meses numero de artículos."""
    template_name = 'blog/article_archive_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {'archive': self._archive_articles()}
        return context

    def _archive_articles(self):
        """Obtiene artículos y los ordena por año."""
        articles = Article.objects.published()
        archive = {}
        date_field = 'create_at'
        years = articles.datetimes(date_field, 'year')[::-1]
        for year in years:
            months = articles.filter(create_at__year=year.year).\
                datetimes(date_field, 'month')
            archive[year] = months
        archive = sorted(archive.items(), reverse=True)
        return archive


class ArticleArchiveMixin(object):
    queryset = Article.objects.published()
    allow_future = False
    make_object_list = True
    date_field = 'create_at'


class ArticleYearArchiveView(ArticleArchiveMixin, YearArchiveView):
    """Mostrar el archivo de artículos por año."""
    template_name = 'blog/article_archive_year.html'


class ArticleMonthArchiveView(ArticleArchiveMixin, MonthArchiveView):
    """Mostrar el archivo de artículos por mes."""
    template_name = 'blog/article_archive_month.html'


class ArticleSubscribeRegisterView(View):
    """Suscribe un email para nuevos artículos."""

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        url_redirect = request.GET.get('next', '/')
        email = request.POST.get('user_email', None)
        try:
            validate_email(email)
            if ArticleSubscribe.objects.filter(email=email):
                messages.error(request, 'Email ya registrado')
            else:
                ArticleSubscribe.objects.create(email=email)
                messages.success(request, 'Email registrado correctamente')
        except ValidationError:
            messages.error(request, 'Email no valido')
        return redirect(url_redirect)


class ArticleSubscribeUnregisterView(View):
    """Unsuscribe un email para nuevos artículos."""

    def get(self, request, *args, **kwargs):
        token_unsigned = kwargs.get('token_unsigned', None)
        if token_unsigned:
            subscribers = ArticleSubscribe.objects.filter(token_unsigned=token_unsigned)
            if subscribers:
                email = subscribers[0].email
                subscribers[0].delete()
                messages.success(request, 'Email {} eliminado!'.format(email))
        return redirect('/')
