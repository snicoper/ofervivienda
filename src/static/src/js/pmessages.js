/**
 * Formulario para mandar mensajes a un usuario.
 *
 * Muestra el botón para "mandar mensaje", si lo pulsa, este
 * se oculta y muestra el formulario.
 *
 * Si le da a cancelar, vuelve a su estado por defecto.
 */
$(document).ready(function () {
  /**
   * Formulario para mandar mensajes a un usuario.
   *
   * Muestra el botón para "mandar mensaje", si lo pulsa, este
   * se oculta y muestra el formulario.
   *
   * Si le da a cancelar, vuelve a su estado por defecto.
   */
  $('#btn-show-form-message').on('click', function () {
    $(this).toggleClass('hidden');
    $('#anuncio-form-message').toggleClass('hidden');
  });

  $('#btn-hide-form-message').on('click', function () {
    $('#anuncio-form-message').toggleClass('hidden');
    $('#btn-show-form-message').toggleClass('hidden');
  });

  /**
   * Comprueba que el formulario al menos tenga mas de X caracteres en
   * subject y message.
   *
   * Para ver cuantos caracteres son cada cosa,
   * @ver: src/apps/pmessages/forms.py
  */
  $('#form-pmessages').on('submit', function (e) {
    const subject = $('#id_subject').val();
    const message = $('#id_body').val();
    let error = false;

    if (subject.length < 5) {
      toastr.error('Minimo 5 caracteres para el titulo');
      error = true;
    }

    if (message.length < 10) {
      toastr.error('Minimo 10 caracteres para el mensaje');
      error = true;
    }

    // Si no hay errores, continuar
    if (error) {
      e.preventDefault();
    }
  });
});
