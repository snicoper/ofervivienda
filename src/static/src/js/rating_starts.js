/**
 * Estrellas con el ratio del resource.
 */
$('.anuncio-rating-stars').each(function (index, value) {
  const self = $(this);
  const readonly = self.data('readonly') === 1;
  const url = self.data('url');
  const messageText = self.data('message-text');
  const messageSuccess = self.data('message-success');

  // En Spanish por ejemplo, separa los decimales con comas.
  value = self.data('value').replace(',', '.');

  // El valor por defecto en caso de no tener votos, es de -1 para que no
  // muestre ninguna estrella.
  if (value === 0) {
    value = -1;
  }

  self.barrating({
    theme: 'fontawesome-stars-o',
    initialRating: value,
    readonly: readonly,
    showSelectedRating: true,

    onSelect (value, text, event) {
      if (typeof(event) !== 'undefined') {
        $.ajax({
          url: url,
          data: { score: value },
          success (data) {
            data = parseFloat(data);
            if (data > 0) {
              const htmlElement = $('.anuncio-user-score');
              const content = `<small>
                ${messageText}${value} <i class="material-icons md-4">star</i>
              </small>`;

              // Actualizar el ratio.
              self.barrating('set', data);
              toastr.success(messageSuccess);

              // Actualizar el score del usuario.
              htmlElement.html(content);
              htmlElement.removeClass('hidden');
            }
          }
        });
      }
    }
  });
});
