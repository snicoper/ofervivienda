from django.test import TestCase
from django.urls import reverse


class CookieConsentViewTest(TestCase):

    def setUp(self):
        super().setUp()
        self.url = 'pages:cookie_consent'
        self.urlconf = reverse(self.url)
        self.response = self.client.get(self.urlconf)

    def test_status_code_200(self):
        """El status_code_200 para todos."""
        self.assertEqual(self.response.status_code, 200)

    def test_templates_usados(self):
        """Prueba el template .md y .html."""
        self.assertTemplateUsed(self.response, 'pages/cookie_consent.html')
        self.assertTemplateUsed(self.response, 'pages/cookie_consent.md')
