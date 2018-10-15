/**
 * En los formularios de viviendas el campo estado_inmueble lo muestra u oculta
 * en función del valor de type_anuncio.
 * Si type_anuncio es 1 (Venta), estado_inmueble sera mostrado.
 * En cualquier otro caso se ocultara.
 *
 * Desde los forms en Django, ya comprueba que dependiendo del valor de
 * type_anuncio, estado_inmueble es un campo requerido o no.
 *
 * Estos formularios se muestran en src/templates/anuncios/anuncio_form.html,
 * tanto en la creación como en la edición.
 */
$(document).ready(function () {
  // Obtener el elemento padre de todo el input.
  const estadoInmueble = $('#id_estado_inmueble').parent();

  function toogleInputTypeAnuncio (e) {
    if (estadoInmueble.length) {
      if (e.val() === 'VENTA' && estadoInmueble.hasClass('hidden')) {
        estadoInmueble.removeClass('hidden');
      } else if (e.val() === 'ALQUILER' && !estadoInmueble.hasClass('hidden')) {
        estadoInmueble.addClass('hidden');
      }
    }
  }

  $('#id_type_anuncio').on('change', function () {
    toogleInputTypeAnuncio($(this));
  });

  toogleInputTypeAnuncio($('#id_type_anuncio'));

  /**
   * Actualizar el campo update_at del anuncio con axios.
   */
  // Previene actualizarlo varias veces.
  let hasUpdate = false;
  $('.field-update-at-anuncio').on('click', function () {
    const self = $(this);
    const url = self.data('url');
    axios.put(url)
      .then((response) => {
        const data = response.data;
        if (data.has_update === true && !hasUpdate) {
          self.children().first().removeClass('text-success');
          self.children().first().removeClass('cursor-pointer');
          self.children().first().addClass('text-warning');
          toastr.success('Se ha actualizado correctamente');
          self.removeClass('field-update-at-anuncio');
          hasUpdate = true;
        }
      });
  });
});
