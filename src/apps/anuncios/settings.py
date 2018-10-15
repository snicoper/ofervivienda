from django.conf import settings

# Tiempo en días que permanecerá un anuncios activo.
# La desactivación se hace con cron.
# @see: ./cron/deactivate_anuncios.py
ANUNCIO_DAYS_ACTIVE = getattr(settings, 'ANUNCIO_DAYS_ACTIVE', 999)

# Cantidad por defecto en las listas de anuncios paginadas
ANUNCIO_PAGINATE_BY = getattr(settings, 'ANUNCIO_PAGINATE_BY', 8)

# Numero máximo de anuncios para un usuario no premium.
ANUNCIO_MAX_ANUNCIOS = getattr(settings, 'ANUNCIO_MAX_ANUNCIOS', 3)

# En detalles de un anuncio, cuantos anuncios relacionados mostrar.
ANUNCIO_NUM_RELACIONADO = getattr(settings, 'ANUNCIO_NUM_RELACIONADO', 6)

# En detalles de un anuncio, buscar relacionados en un radio kms.
ANUNCIO_RELACIONADO_KMS = getattr(settings, 'ANUNCIO_RELACIONADO_KMS', 3)

# Tiempo mínimo antes de poder actualizar el anuncio, create_at.
ANUNCIO_MIN_DAYS_UPLOAD_UPDATE_AT = getattr(settings, 'ANUNCIO_MIN_DAYS_UPLOAD_UPDATE_AT', 3)
