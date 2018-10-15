from django import forms

from .models import Message


class MessageCreateForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['parent', 'anuncio', 'sender', 'recipient', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].widget = forms.HiddenInput()
        self.fields['anuncio'].widget = forms.HiddenInput()
        self.fields['sender'].widget = forms.HiddenInput()
        self.fields['recipient'].widget = forms.HiddenInput()

    def clean(self):
        """Como el form esta oculto, los errores se informan de manera global
        para que sean mostrados en el toast de materialize.

        @see: src/static/src/js/pmessages.js
        """
        cleaned_data = super().clean()
        subject = cleaned_data.get('subject')
        body = cleaned_data.get('body')
        if not subject or len(subject) < 5:
            msg_error = 'El asunto es demasiado corto, al menos 10 caracteres'
            raise forms.ValidationError(msg_error)
        if not body or len(body) < 10:
            msg_error = 'El mensaje es demasiado corto, al menos 10 caracteres'
            raise forms.ValidationError(msg_error)
        return cleaned_data
