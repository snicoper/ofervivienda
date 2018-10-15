from django.conf import settings

##################################
# Images anuncios normales
##################################

# Image max width
GALLERY_IMAGE_WIDTH = getattr(settings, 'GALLERY_IMAGE_WIDTH', 600)

# Image max height
GALLERY_IMAGE_HEIGHT = getattr(settings, 'GALLERY_IMAGE_HEIGHT', 600)

# Calidad de la imagen.
GALLERY_IMAGE_QUALITY = getattr(settings, 'GALLERY_IMAGE_QUALITY', 60)

##################################
# Images anuncios Premium
##################################

# Image max width
GALLERY_IMAGE_PREMIUM_WIDTH = getattr(settings, 'GALLERY_IMAGE_PREMIUM_WIDTH', 1000)

# Image max height
GALLERY_IMAGE_PREMIUM_HEIGHT = getattr(settings, 'GALLERY_IMAGE_PREMIUM_HEIGHT', 1000)

# Calidad de la imagen.
GALLERY_IMAGE_QUALITY_PREMIUM = getattr(settings, 'GALLERY_IMAGE_QUALITY', 90)

################################################################
# Images anuncios Premium/normales
# Importante no cambiar los tamaños, puede desajustar las cards.
################################################################

# Numero máximo de imágenes por anuncio.
IMAGES_MAX_IMAGES = getattr(settings, 'IMAGES_MAX_IMAGES', 5)

# PATH guarda image
GALLERY_IMAGE_PATH = getattr(settings, 'GALLERY_IMAGE_PATH', 'anuncios/')

# Thumbnail max width
GALLERY_THUMBNAIL_WIDTH = getattr(settings, 'GALLERY_THUMBNAIL_WIDTH', 300)

# Thumbnail max height
GALLERY_THUMBNAIL_HEIGHT = getattr(settings, 'GALLERY_THUMBNAIL_HEIGHT', 200)

# PATH y prefijo donde guarda thumbnail
GALLERY_THUMBNAIL_PATH = getattr(settings, 'GALLERY_IMAGE_PATH', 'anuncios/thumbnail_{}')

# Default thumbnail si no tiene imágenes.
GALLERY_THUMBNAIL_DEFAULT = getattr(settings, 'GALLERY_THUMBNAIL_DEFAULT', 'dummy-image.jpg')
