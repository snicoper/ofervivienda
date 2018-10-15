#!/usr/bin/env python

# Comprueba las cuentas premium, si han expirado,
# se pondrá al usuario como normal.

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Add BASE_DIR and BASE_DIR/apps to $PYTHONPATH.

sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.config.settings.prod')

import django
django.setup()

####################################################################################################
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

now = timezone.now()

expired_users = User.objects.filter(
    is_premium=True,
    expire_premium_at__lte=now
).update(is_premium=False)

print('Cuentas Premium expiradas, is_premium = False con éxito')
