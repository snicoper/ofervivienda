===========
Description
===========

Crear un sistema para poder crear anuncios inmobiliarios.

Un anunciante podrá crear anuncios de manera gratuita hasta un máximo de
``src/apps/anuncios/settings.ANUNCIO_MAX_ANUNCIOS`` anuncios.

* Los anuncios se podrán convertir en anuncios premium en cualquier momento.
* Los anuncios podrán ser activados y desactivados.
* Los anuncios se le podrá actualizar el campo ``update_at``, solo si el anuncio es premium.

Método de ordenación y update_at
================================

La ordenación de los anuncios dependen del campo ``ordering`` en la clase ``Meta``
del modelo :mod:`anuncios.models.Anuncio`, esta es la ordenación que tiene:

.. code-block:: python

    ordering = ('-active', '-is_premium', '-update_at')

Eso significa que primero los ``active=True``, después los anuncios ``premium``
y por ultimo, ordenados por fecha en el campo ``update_at``.

El campo ``update_at``, siempre se ha de actualizar de manera **explicita** por
el usuario, pero hay algunas reglas para que el usuario pueda actualizar el anuncio.

* **Primera regla:** El anuncio ha de ser un **anuncio premium**.
* **Segunda regla:** El anuncio no puede actualizarse si no ha pasado ``src/apps/anuncios/settings.ANUNCIO_MIN_DAYS_UPLOAD_UPDATE_AT`` días desde que se publico o desde su ultima actualización manual del anuncio.

La actualización se hace desde los templates, en concreto desde **detalles del anuncio**
en el archivo ``src/apps/anuncios/templates/anuncios/details.html``.

Se hace con **Jquery** y el archivo **JavaScript** es ``src/static/src/js/anuncios.js``
con el evento ``$('.field-update-at-anuncio').on('click', function() {});``

Para obtener si el anuncio y usuario puede actualizar el anuncios, se hace desde
el **templatetags** de anuncios, desde ``anuncios_tags.py`` y la función
``can_upload_update_at``.

Una vez que se ha actualizado el anuncio, el anuncio pasara a ponerse en primera
posición (ya que siempre es premium) en las búsquedas.

Esta es la única manera de poder actualizar el campo ``update_at`` y no confundir
con ``active=False|True``.

Creación de un anuncio gratis
=============================

A la hora de creación de un anuncio, si el anuncio es gratis, solo sera gratis
si tiene menos anuncios de ``settings.ANUNCIO_MAX_ANUNCIOS``.

Da igual cuantos anuncios tenga, solo **probara los anuncios que no sean premium**.

Pasar el anuncio a premium
==========================

Dar la posibilidad de un anuncio pueda pasar de normal a premium. Para ello,
habrá 2 maneras de hacerlo, o bien el usuario es o se hace premium y luego
convierte el/los anuncio/s en premium o bien compra uno/varios anuncios premium
desde la perfil de usuario.

Si convierte la cuenta en premium, todos los anuncios que tenga puestos, podrá
pasarlos a anuncios premium.

Si lo que quiere es un anuncio (o varios) anuncios premium, también tiene la
posibilidad de hacerlo por un numero de anuncios.

Activar desactivar un anuncio
=============================

Un usuario puede poner el anuncio como ``active=False`` y de esta manera
"ocultarlos" al resto de usuarios.

Los anuncios **inactivos**, cuentan como anuncios para "los anuncios gratis"
pero no como anuncios gratis activos, es decir si tiene 3 anuncios gratis y 2
premium y solo 1 anuncio gratis inactivo, el anuncio gratis inactivo podrá activarlo.

Diferencias anuncios premium y anuncio normal
=============================================

Hay dos tipos de anuncios, los premium y los normales y las diferencias son:

* Las imágenes de los anuncios tendrán una mayor resolución.
* Todas las imágenes que quieras en cada anuncio.
* Los posicionamientos en las búsquedas siempre estarán por encima de los anuncios normales.
* Actualizar el anuncio cada ``ANUNCIO_MIN_DAYS_UPLOAD_UPDATE_AT`` días.

Máximo de anuncios normales por anunciante
==========================================

El máximo de anuncios gratis por anunciante es ``settings.ANUNCIO_MAX_ANUNCIOS``,
de manera predeterminada es ``3``
