/**
 * Cuando cambia el campo category a habitación, el campo type_anuncio cambia
 * a alquiler.
 */
(function () {
  function changeInitialFieldTypeAnuncio () {
    let category = $('#id_category').val();
    let typeAnuncio = $('#id_type_anuncio');

    if (category === 'HABITACION') {
      typeAnuncio.val('ALQUILER');
    }
  }

  $('#id_category').on('change', function () {
    changeInitialFieldTypeAnuncio();
  });

  // En caso de recarga la pagina, inicializar valores.
  changeInitialFieldTypeAnuncio();
})();
