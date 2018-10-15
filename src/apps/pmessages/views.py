from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import Http404, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView

from .forms import MessageCreateForm
from .models import Message
from .utils import notify_new_pmessage


class MessageInboxView(LoginRequiredMixin, ListView):
    template_name = 'pmessages/inbox.html'
    context_object_name = 'inbox_list'
    paginate_by = 10
    model = Message

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(recipient=self.request.user)
        return queryset.select_related('parent', 'sender', 'anuncio', 'recipient')


class MessageOutboxView(LoginRequiredMixin, ListView):
    template_name = 'pmessages/outbox.html'
    context_object_name = 'outbox_list'
    paginate_by = 10
    model = Message

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(sender=self.request.user)
        return queryset.select_related('parent', 'sender', 'anuncio', 'recipient')


class ThreadListView(ListView):
    template_name = 'pmessages/thread.html'
    context_object_name = 'thread_list'
    paginate_by = 10
    model = Message

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = None

    def dispatch(self, request, *args, **kwargs):
        """Solo lo pueden ver sender y recipient."""
        self.message = get_object_or_404(Message, pk=kwargs.get('pk'))
        if request.user != self.message.sender and request.user != self.message.recipient:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Obtener lista de mensajes de un thread y marcar como leídos."""
        message_list = Message.objects.get_thread(self.kwargs.get('pk'))
        message_list.filter(recipient=self.request.user).update(recipient_read=True)
        return message_list.select_related('parent', 'sender', 'anuncio', 'recipient')

    def get_context_data(self, **kwargs):
        """Obtener el form para responder al thread."""
        context = super().get_context_data(**kwargs)
        parent = self.message.parent if self.message.parent else self.message
        form = MessageCreateForm(self.request.POST or None)

        # Si el sender parent es igual al usuario, mandara de nuevo otro
        # mensaje al parent recipient.
        if parent.sender == self.request.user:
            sender = parent.sender
            recipient = parent.recipient
        else:
            sender = parent.recipient
            recipient = parent.sender
        if 'RE: ' in self.message.subject:
            subject = self.message.subject
        else:
            subject = 'RE: {}'.format(self.message.subject)
        form.initial['parent'] = parent
        form.initial['anuncio'] = self.message.anuncio
        form.initial['sender'] = sender
        form.initial['recipient'] = recipient
        form.initial['subject'] = subject
        form.fields['subject'].widget = forms.HiddenInput()
        context['form'] = form
        context['btn_form_message'] = 'Responder'
        return context


class MessageCreateView(LoginRequiredMixin, CreateView):
    form_class = MessageCreateForm
    http_method_names = ['post']
    model = Message

    def http_method_not_allowed(self, request, *args, **kwargs):
        raise Http404

    def form_invalid(self, form):
        """Si hay un error en el form, redirecciona al form.

        Los datos se perderán, por lo que hay que asegurarse con js de que tenga
        subject y body un mínimo de caracteres.
        """
        redirect_to = self.request.POST.get('next', reverse('pmessages:inbox'))
        return redirect(redirect_to)

    def get_success_url(self):
        msg_success = 'Se ha enviado el mensaje con éxito'
        messages.success(self.request, msg_success)
        redirect_to = self.request.POST.get('next', reverse('pmessages:inbox'))
        notify_new_pmessage(self.request, self.object)
        return redirect_to
