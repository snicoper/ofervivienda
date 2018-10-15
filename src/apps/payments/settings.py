from django.conf import settings

# Precio Premium 1 mes
PAYMENTS_PREMIUM1 = getattr(settings, 'PAYMENTS_PREMIUM1', 7.00)

# Precio Premium 3 meses (5%)
PAYMENTS_PREMIUM3 = getattr(settings, 'PAYMENTS_PREMIUM3', 19.95)

# Precio Premium 6 meses (8%)
PAYMENTS_PREMIUM6 = getattr(settings, 'PAYMENTS_PREMIUM6', 38.64)

# Precio Premium 12 meses (12%)
PAYMENTS_PREMIUM12 = getattr(settings, 'PAYMENTS_PREMIUM12', 73.92)

# Precio Anuncio Premium
PAYMENTS_ANUNCIO = getattr(settings, 'PAYMENTS_ANUNCIO', 2.00)
