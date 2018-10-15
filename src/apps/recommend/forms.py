from django import forms


class RecommendForm(forms.Form):
    """Form para recomendar un anuncio."""
    email_to = forms.EmailField(
        label='Email destinatario'
    )
    from_email = forms.EmailField(
        label='Tu email'
    )
    body = forms.CharField(
        label='Mensaje',
        widget=forms.Textarea(),
        required=False
    )
