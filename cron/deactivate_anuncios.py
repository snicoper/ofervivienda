#!/usr/bin/env python

# Desactiva los anuncios caducados.

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Add BASE_DIR and BASE_DIR/apps to $PYTHONPATH.

sys.path.insert(0, BASE_DIR)

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.config.settings.prod')

import django
django.setup()
