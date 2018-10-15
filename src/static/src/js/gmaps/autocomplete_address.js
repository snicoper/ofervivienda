/**
 * Muestra Autocomplete de gmaps
 */
function initAddressAutocomplete () {
  $(document).ready(function () {
    new google.maps.places.Autocomplete(document.querySelector('#id_q'));
  });
}
