/**
 * Comprueba según la dirección, obtiene lat y lng y los añade en los campos
 * hidden del formulario.
 *
 * Si el formulario tiene algún campo vació, hará un submit y Django sera el
 * encargado de comprobar los requerimientos.
 *
 * Si el status de geocoder.geocode() no es google.maps.GeocoderStatus.OK,
 * representa que la dirección que ha puesto no es valida y se notificara con
 * un error.
 */
$('#form-location-to-coords').on('click', function () {
  const geocoder = new google.maps.Geocoder();
  let address = [];

  address.push(document.querySelector('#id_country').value);
  address.push(document.querySelector('#id_state').value);
  address.push(document.querySelector('#id_city').value);
  address.push(document.querySelector('#id_address').value);

  for (let i = 0; i < address.length; i++) {
    if (address[i] === '') {
      $('#form-location').submit();
    }
  }

  address = address.join(', ');

  geocoder.geocode({ 'address': address }, (results, status) => {
    const messageError = 'La dirección no parece valida, revisa la por favor';

    if (status === google.maps.GeocoderStatus.OK) {
      document.querySelector('#id_latitude').value = results[0].geometry.location.lat();
      document.querySelector('#id_longitude').value = results[0].geometry.location.lng();
      $('#form-location').submit();
    } else {
      // Si la dirección no parece valida, notificar al usuario.
      toastr.error(messageError);
    }
  });
});
