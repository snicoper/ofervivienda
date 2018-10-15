/**
 * Obtener localización del usuario con geolocation del navegador.
 * Guarda los datos en localStorage.
 *
 * localStorage.getItem('latitude|longitude')
 *
 *
 * NOTA: En desarrollo para ver como funciona, se ha de entrar con la
 * IP publica.
 */
const el = $('#user-lat-lng');
let userLatitude = 0;
let userLongitude = 0;

if ('geolocation' in navigator) {
  navigator.geolocation.getCurrentPosition(function (position) {
    // Si existe latitude, es que ya tiene coords guardadas.
    if (!localStorage.getItem('latitude')) {
      localStorage.setItem('latitude', position.coords.latitude);
      localStorage.setItem('longitude', position.coords.longitude);
    }
  });
}

// Ver si hay un campo de formulario con latitude y longitude.
const latitudeInput = document.querySelector('#id_latitude');
const longitudeInput = document.querySelector('#id_longitude');

/**
 * Intentar obtener latitude y longitude para posicionar el mapa,
 *
 * La precedencia es:
 * - Campo de formulario.
 * - Obtenida del navegador.
 * - Configuración del usuario en el perfil.
 * - freegeoip.net
 * - Una por defecto (Madrid).
 */

// Campo de formulario.
if (!userLatitude && latitudeInput) {
  userLatitude = parseFloat(latitudeInput.value.replace(',', '.')) || userLatitude;
  userLongitude = parseFloat(longitudeInput.value.replace(',', '.')) || userLongitude;
}

// Con el objeto navigator.geolocation o localStorage.
if (localStorage.getItem('latitude')) {
  userLatitude = localStorage.getItem('latitude') || userLatitude;
  userLongitude = localStorage.getItem('longitude') || userLongitude;
}

// Configuración del usuario en el perfil.
// Obtenida de src/templates/_gmaps_script.html
if (userLatitude === 0) {
  userLatitude = parseFloat(el.data('user-latitude')) || userLatitude;
  userLongitude = parseFloat(el.data('user-longitude')) || userLongitude;
}

/**
 * Ultimo intento antes de poner una localización por defecto.
 * freegeoip.net
 *
 * @see: src/apps/utils/api.py y src/config/urls.py
 */
if (userLatitude === 0) {
  $.ajax({
    url: '/api/user-ip-info/',
    dataType: 'json',
    method: 'GET',

    success (data) {
      if (data !== 'BAD') {
        userLatitude = data.latitude || userLatitude;
        userLongitude = data.longitude || userLongitude;
      }
    },
  });
}

// Una por defecto (Madrid).
if (userLatitude === 0) {
  userLatitude = 40.416775;
  userLongitude = -3.703790;
}
