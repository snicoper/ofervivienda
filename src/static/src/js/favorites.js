/**
 * Añade un anuncio a favoritos via AJAX.
 * Usado en src/templates/favorites/_heart_favorites.html
 */
$('.add-anuncio-favorite').on('click', function () {
  const self = $(this);
  const anuncioId = self.data('anuncio-id');
  const url = self.data('url');
  const message = '¡Anuncio añadido a favoritos!';

  $.ajax({
    method: 'POST',
    url: url,
    data: {
      anuncio_id: anuncioId
    }
  })
    .done(function (data) {
      if (data.add === true) {
        toastr.success(message);
        self.toggleClass('hidden');
        self.siblings().toggleClass('hidden');
      }
    });
});

/**
 * Elimina un anuncio de favoritos via AJAX.
 * Usado en src/templates/anuncios/details.html
 */
$('.remove-anuncio-favorite').on('click', function () {
  const self = $(this);
  const anuncioId = self.data('anuncio-id');
  const url = self.data('url');
  const message = '¡Anuncio eliminado de favoritos!';

  $.ajax({
    method: 'POST',
    url: url,
    data: {
      anuncio_id: anuncioId
    }
  })
    .done(function (data) {
      if (data.remove === true) {
        toastr.warning(message);
        self.toggleClass('hidden');
        self.siblings().toggleClass('hidden');
      }
    });
});
