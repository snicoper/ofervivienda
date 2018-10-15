from django.conf import settings

# Días de expiración de un código de promoción.
PROMO_EXPIRE_DAYS = getattr(settings, 'PROMO_EXPIRE_DAYS', 30)
