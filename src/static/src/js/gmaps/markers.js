/**
 * Marca una posición en el mapa
 * @param  {element} elementData Elemento contenedor principal,
 *                               require de data-latitude y data-longitude.
 * @param  {element} elementMap  Div contenedor donde mostrar el mapa.
 * @return {map} El objeto map.
 */
function markPositionOnMap (elementData, elementMap) {
  const latitude = parseFloat(elementData.data('latitude').replace(',', '.'));
  const longitude = parseFloat(elementData.data('longitude').replace(',', '.'));
  const zoom = 18;
  const latLng = new google.maps.LatLng(latitude, longitude);

  const map = new google.maps.Map(document.getElementById(elementMap), {
    zoom: zoom,
    center: latLng,
    disableDefaultUI: true,
    zoomControl: true
  });

  new google.maps.Marker({
    position: latLng,
    map: map,
    icon: 'http://www.codeshare.co.uk/images/blue-pin.png'
  });

  /**
   * Recarga el mapa en el lienzo.
   */
  function reloadMap () {
    const lastCenter = map.getCenter();
    google.maps.event.trigger(map, 'resize');
    map.setCenter(lastCenter);
  }

  /**
   * Es necesario para mostrarlo en el modal.
   * Obtener lastCenter para que si se abre varias veces, centre la posición.
   * De lo contrario lo mostrara descentrado.
   */
  $('#map-modal').on('shown.bs.modal', function () {
    reloadMap();
  });
}

/**
 * Marca una posición de Google Maps.
 * Lo marca en un modal.
 *
 * El botón que activa el evento, debe tener data-tatitude y
 * data-longitude donde mostrara el marker.
 *
 * En la pagina que lo marca, debe tener link a la api de gmaps.
 * También tiene que tener el modal ->
 * {% include '_modal_gmaps.html' %} antes de </body>
 *
 * Fuentes:
 * http://stackoverflow.com/questions/35698042/how-to-load-google-map-in-materialize-modal
 * http://stackoverflow.com/questions/12077161/google-map-does-not-center-even-after-resize
*/
if ($('.set-position-gmaps').length) {
  $('.set-position-gmaps').on('click', function () {
    markPositionOnMap($(this), 'map');
  });
}
