#!/usr/bin/env python
# flake8: noqa

# Para pruebas rapidas

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.config.settings.local')

import django
django.setup()

##############################################################################
from anuncios.models import AnuncioPiso

a = AnuncioPiso.objects.first()
print(a.get_ratio)
