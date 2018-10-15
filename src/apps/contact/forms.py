from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Formulario de contacto base."""

    class Meta:
        model = ContactMessage
        fields = (
            'subject',
            'username',
            'email',
            'message',
            'screenshot',
            'is_register'
        )
        help_texts = {
            'screenshot': 'Aportar imagen'
        }
