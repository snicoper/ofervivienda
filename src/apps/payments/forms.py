from django import forms
from django.conf import settings


class PaypalIpnForm(forms.Form):
    """Form para IPN de PayPal."""
    cmd = forms.CharField(
        widget=forms.HiddenInput(),
        initial='_xclick'
    )
    business = forms.CharField(
        widget=forms.HiddenInput(),
        initial=settings.PAYPAL_RECEIVER_EMAIL
    )
    charset = forms.CharField(
        widget=forms.HiddenInput(),
        initial='utf-8'
    )
    amount = forms.CharField(
        widget=forms.HiddenInput()
    )
    currency_code = forms.CharField(
        widget=forms.HiddenInput(),
        initial='EUR'
    )
    item_name = forms.CharField(
        widget=forms.HiddenInput()
    )
    item_number = forms.CharField(
        widget=forms.HiddenInput()
    )
    invoice = forms.EmailField(
        widget=forms.HiddenInput()
    )
    custom = forms.CharField(
        widget=forms.HiddenInput()
    )
    notify_url = forms.URLField(
        widget=forms.HiddenInput()
    )
    return_url = forms.URLField(
        widget=forms.HiddenInput()
    )
    cancel_return = forms.URLField(
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['return'] = self.fields['return_url']
        del self.fields['return_url']
