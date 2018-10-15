from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.geos import GEOSGeometry, Point
from django.contrib.gis.measure import Distance
from django.db.models import Avg
from django.shortcuts import Http404, get_object_or_404, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import (
    CreateView, DetailView, ListView, RedirectView, TemplateView, UpdateView,
    View,
)

from alerts.utils import alerts_users_new_anuncio
from anuncios.mixins.views import ClassFromCategoryNameMixin, ClassFromIDMixin
from favorites.mixins.views import FavoriteListContextMixin
from pmessages.forms import MessageCreateForm

from . import settings as anuncios_settings
from .forms import BaseAnuncioForm
from .models import Anuncio

UserModel = get_user_model()


class BaseAnuncioListView(FavoriteListContextMixin, ListView):
    """Base para listado de anuncios."""
    paginate_by = anuncios_settings.ANUNCIO_PAGINATE_BY
    context_object_name = 'anuncio_list'
    model = Anuncio

    def get_queryset(self):
        """Obtener la lista de anuncios active=True."""
        return self.model.objects.published().select_related(
            'owner'
        ).prefetch_related('image_anuncio').select_subclasses()


class AnuncioListView(BaseAnuncioListView):
    """Lista de los últimos anuncios."""
    template_name = 'anuncios/list.html'


class AnuncioListByOwnerView(BaseAnuncioListView):
    """Lista de anuncios de un usuario."""
    template_name = 'anuncios/list_owner.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def dispatch(self, request, *args, **kwargs):
        """Si no existe id usuario, lanzara Http404."""
        self.user = get_object_or_404(UserModel, slug=kwargs.get('slug'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Añadir el owner del anuncio al contexto."""
        context = super().get_context_data(**kwargs)
        context['owner'] = self.user
        return context

    def get_queryset(self):
        """Obtiene el queryset según usuario.

        Si es owner de los anuncios, le mostrara los active=False, de lo
        contrario, solo mostrara los active=True.
        """
        if self.user == self.request.user:
            queryset = self.model.objects.filter(owner=self.user).select_subclasses().\
                select_related('owner').prefetch_related('image_anuncio')
        else:
            queryset = super().get_queryset().filter(owner=self.user)
        return queryset


class AnuncioDetailView(ClassFromIDMixin, FavoriteListContextMixin, DetailView):
    """Detalles de un anuncio."""
    template_name = 'anuncios/details.html'
    context_object_name = 'anuncio'
    model = Anuncio

    def dispatch(self, request, *args, **kwargs):
        """Solo el owner puede ver anuncios desactivados."""
        obj = self.get_object()
        if not obj.active and obj.owner != request.user:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Añade el campo ratio al anuncio."""
        queryset = super().get_queryset()
        return queryset.annotate(
            ratio=Avg('ratio_anuncio__score')
        ).select_related('owner').prefetch_related('image_anuncio', 'ratio_anuncio')

    def get_context_data(self, **kwargs):
        """Añade variables de contexto.

        Incrementa en 1 anuncio.views.

        Añade las siguientes variables de contexto:
            - form (MessageCreateForm): Formulario de contacto.
            - anuncios_related_list (queryset[Anuncio]): Anuncios del mismo tipo en la zona.
            - favorite_list_by_owner (list): PKs con los favoritos del usuario
              desde FavoriteListContextMixin.
        """
        context = super().get_context_data(**kwargs)
        anuncio = self.object
        # Incrementar en 1 las vistas del anuncio.
        # Omitir si es superuser o si el usuario es el owner.
        if not self.request.user.is_superuser and anuncio.owner != self.request.user:
            anuncio.views += 1
            anuncio.save()
        # Form de contacto.
        form = MessageCreateForm(self.request.POST or None)
        form.initial['anuncio'] = anuncio
        form.initial['sender'] = self.request.user
        form.initial['recipient'] = anuncio.owner
        context['form'] = form
        # Anuncios del mismo tipo en la misma zona.
        distance = anuncios_settings.ANUNCIO_RELACIONADO_KMS
        point = Point(anuncio.longitude, anuncio.latitude)
        anuncios_related_list = Anuncio.get_model_class(
            anuncio.category
        ).objects.published(
            type_anuncio=anuncio.type_anuncio,
            point__distance_lt=(point, Distance(km=distance))
        ).exclude(
            pk=anuncio.pk
        ).select_related(
            'owner'
        ).prefetch_related(
            'image_anuncio'
        )[0:anuncios_settings.ANUNCIO_NUM_RELACIONADO]
        context['anuncios_related_list'] = anuncios_related_list
        return context


class AnuncioCreateSelectListView(LoginRequiredMixin, TemplateView):
    """Muestra select con las categorías."""
    template_name = 'anuncios/create_select_list.html'

    def get_context_data(self, **kwargs):
        """Añadir categorías para el form."""
        context = super().get_context_data(**kwargs)
        context['category_list'] = {k: v for k, v in Anuncio.CATEGORY_CHOICES}
        return context


class AnuncioFormViewMixin(ClassFromCategoryNameMixin, LoginRequiredMixin):
    """Base para anuncios con formulario.

    Tanto los update como los create.
    Requiere login de usuario, después ya cada views se encarga en comprobar
    otros permisos.

    Attributes:
        title (str): Titulo a mostrar en el template.
        btn_form_name (str): Nombre del botón 'submit' del formulario.
    """
    template_name = 'anuncios/form.html'
    context_object_name = 'anuncio'
    model = Anuncio

    @property
    def title(self):
        raise NotImplementedError

    @property
    def btn_form_name(self):
        raise NotImplementedError

    def get_form_class(self):
        """Obtiene la clase de form por category."""
        return BaseAnuncioForm.get_form_class(self.category)

    def get_context_data(self, **kwargs):
        """Añade contexto al form.

        title (str): Titulo de la pagina.
        btn_form_name (str): Nombre del botón submit del formulario.
        category_name (str): Nombre de la categoría (value).
        category (str): Nombre de la categoría (UPPERCASE).

        La diferencia entre category_name y category es que uno muestra el 'key'
        y el otro el 'value'.
        CATEGORY_CHOICES = (
            ('CATEGORY', 'Category name'),
        )
        """
        category_name = {k: v for k, v in Anuncio.CATEGORY_CHOICES}
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['btn_form_name'] = self.btn_form_name
        context['category_name'] = category_name.get(self.category)
        context['category'] = self.category
        return context

    def form_valid(self, form):
        """Añadir POINT al objeto."""
        instance = form.save(commit=False)
        latitude = form.cleaned_data['latitude']
        longitude = form.cleaned_data['longitude']
        instance.point = GEOSGeometry('POINT({} {})'.format(longitude, latitude))
        instance.save()
        return super().form_valid(form)


class AnuncioCreateView(AnuncioFormViewMixin, CreateView):
    """Form para crear anuncios."""
    btn_form_name = 'Crear'
    title = 'Crear anuncio'

    def dispatch(self, request, *args, **kwargs):
        """Comprobar que puede poner un anuncio.

        Comprueba si es usuario premium o si tiene menos de ANUNCIO_MAX_ANUNCIOS.
        El superuser, no tiene limites.
        """
        if request.user.is_authenticated and not request.user.is_superuser:
            # Solo cuenta los anuncios normales, los premium los omite.
            anuncios_count = self.model.objects.filter(
                owner=request.user,
                is_premium=False
            ).count()
            if (not (request.user.is_premium or request.user.anuncios_premium) and
                    anuncios_count >= anuncios_settings.ANUNCIO_MAX_ANUNCIOS):
                messages.warning(request, 'Has llegado al máximo de anuncios')
                return redirect('payments:process_anuncio_premium')
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        """Añade el id usuario y la categoría a los campos del form.

        Si el usuario tiene la opción de usuario 'phone_public' y añadido un
        phone como principal, también se añadirá a initial.

        Si el usuario es premium o tiene anuncios_premium, el anuncio se
        convierte en premium.
        """
        initial = super().get_initial().copy()
        initial['category'] = self.category
        initial['owner'] = self.request.user.id
        if self.request.user.user_options.phone_public and self.request.user.phone:
            initial['phone'] = self.request.user.phone
        if self.request.user.is_premium or self.request.user.anuncios_premium:
            initial['is_premium'] = True

        # Si el usuario tiene localización en su perfil, ponemos
        # por defecto algunos datos en el form con su localización.
        user_location = self.request.user.user_location
        if user_location.latitude:
            initial['country'] = user_location.country
            initial['state'] = user_location.state
            initial['city'] = user_location.city
        return initial

    def get_success_url(self):
        """Actualizar user.anuncios_premium.

        Si el anuncio ha utilizado anuncios_premium del usuario, se ha de
        decrementar en 1. Si el usuario tiene una cuenta premium y también
        anuncios_premium, no se decrementara.

        Redirecciona a las imágenes para que pueda añadirlas.

        Alertara a los usuarios con una coincidencia en el anuncio actual.
        """
        alerts_users_new_anuncio(self.object, self.request)
        if not self.request.user.is_premium and self.request.user.anuncios_premium:
            self.request.user.decrease_anuncio()
            self.request.user.save()
        msg_success = 'El anuncio ha sido creado con éxito'
        messages.success(self.request, msg_success)
        return reverse('gallery:image_anuncio_add', kwargs={'id_anuncio': self.object.pk})


class AnuncioUpdateView(AnuncioFormViewMixin, UpdateView):
    """Formulario para actualizar un anuncio."""
    btn_form_name = 'Actualizar'
    title = 'Actualizar anuncio'

    def dispatch(self, request, *args, **kwargs):
        """Comprueba que el que quiere editar el anuncio, es el propietario."""
        if self.get_object().owner.id != request.user.id:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        msg_success = 'El anuncio ha sido actualizado con éxito'
        messages.success(self.request, msg_success)
        return super().get_success_url()


class BaseAnuncioToggleView(LoginRequiredMixin, RedirectView):
    """Mixin para activar/desactivar anuncios.

    Attributes:
        action (str): Acción del anuncio activate|deactivate.
    """
    http_method_names = ['get']

    @property
    def action(self):
        raise NotImplementedError

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.anuncio = None

    def dispatch(self, request, *args, **kwargs):
        """Comprueba que el anuncio exista y el usuario es el owner."""
        id_anuncio = kwargs.get('id_anuncio')
        self.anuncio = get_object_or_404(Anuncio, pk=id_anuncio)
        if self.anuncio.owner.pk != request.user.id:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Activa/Desactiva un anuncio.

        Obteniendo self.action, activa o desactiva el anuncio.
        """
        anuncio = Anuncio.objects.get(pk=self.anuncio.pk)
        save_object = False
        message = ''
        if self.action == 'deactivate' and anuncio.active is True:
            anuncio.active = False
            save_object = True
            message = 'desactivado'
        elif self.action == 'activate' and anuncio.active is False:
            anuncio.active = True
            save_object = True
            message = 'activado'
        if save_object:
            anuncio.save()
            msg_success = 'El anuncio ha sido {} con éxito.'.format(message)
            messages.success(request, msg_success)
        else:
            message_info = 'No hay cambios a realizar'
            messages.info(request, message_info)
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        """Redirecciona a ?next= o a detalles del anuncio."""
        redirect_to = self.request.GET.get(
            'next',
            reverse('anuncios:details', kwargs={'pk': self.anuncio.pk})
        )
        return redirect_to

    def http_method_not_allowed(self, request, *args, **kwargs):
        raise Http404


class AnuncioDeactivateView(BaseAnuncioToggleView):
    """Desactiva un anuncio."""
    action = 'deactivate'


class AnuncioActivateView(BaseAnuncioToggleView):
    """Activa un anuncio."""
    action = 'activate'

    def get(self, request, *args, **kwargs):
        """Comprueba si puede activar el anuncio.

        Lo puede activar si es una de estas situaciones:
        - El usuario es premium.
        - El anuncio es premium.
        - Tiene menos de ANUNCIO_MAX_ANUNCIOS (Omite los anuncios premium).
        """
        # Si el anuncio ya esta activo, redirecciona al anuncio de nuevo.
        if self.anuncio.active:
            return super().get(request, *args, **kwargs)
        raise_http404 = True
        user = request.user
        anuncios_user_count = Anuncio.objects.filter(
            owner=user,
            active=True,
            is_premium=False
        ).count()
        if user.is_premium or self.anuncio.is_premium:
            raise_http404 = False
        if raise_http404 and anuncios_user_count < anuncios_settings.ANUNCIO_MAX_ANUNCIOS:
            raise_http404 = False
        if raise_http404:
            msg_warning = mark_safe(
                'Ya tienes activo el máximo de anuncios.<br>'
                'Si quieres activarlo, es necesario adquirir un anuncio premium.'
            )
            messages.warning(request, msg_warning)
            return redirect(reverse('payments:process_anuncio_premium'))
        return super().get(request, *args, **kwargs)


class AnuncioConvertPremiumView(LoginRequiredMixin, View):
    """Hay dos maneras de llegar, GET y POST, con GET significa que el usuario
    no es premium ni tiene anuncios_premium y redirecciona a la pagina de proceso
    de "anuncio premium" para informar de las ventajas de convertirlo en premium.

    Si llega por method POST, significa que el usuario es premium o
    tiene anuncios_premium, por lo que el anuncio pasara a ser premium.
    """
    template_name = 'payments/process_anuncio_premium.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.anuncio = None

    def dispatch(self, request, *args, **kwargs):
        """Comprueba que el anuncio exista y el usuario es el owner."""
        id_anuncio = kwargs.get('id_anuncio')
        self.anuncio = get_object_or_404(Anuncio, pk=id_anuncio)
        if self.anuncio.owner.pk != request.user.id:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return redirect(reverse('payments:process_anuncio_premium'))

    def post(self, request, *args, **kwargs):
        """Convierte el anuncio a Premium."""
        # Si no existe can_activate redirecciona al anuncio.
        # can_activate obtenido de
        # src/apps/anuncios/templates/anuncios/_panel_owner_anuncio.html
        if not request.POST.get('can_activate') or self.anuncio.is_premium:
            return redirect(self.get_redirect_url())
        # Si es usuario premium, aunque tenga anuncios premium, no se
        # le descuentan.
        anuncio_activate = False
        if not request.user.is_premium and request.user.anuncios_premium:
            self.anuncio.is_premium = True
            self.anuncio.save()
            request.user.decrease_anuncio()
            request.user.save()
            anuncio_activate = True
        if request.user.is_premium:
            self.anuncio.is_premium = True
            self.anuncio.save()
            anuncio_activate = True
        if anuncio_activate:
            msg_success = 'El anuncio se ha convertido en premium'
            messages.success(request, msg_success)
        return redirect(self.get_redirect_url())

    def get_redirect_url(self):
        """Redirecciona a detalles del anuncio."""
        return reverse('anuncios:details', kwargs={'pk': self.anuncio.pk})
