/*
  global longitudeInput, latitudeInput, userLatitude, userLongitude,
         imageAnuncio
*/

/**
 * Inicializa el mapa para búsqueda avanzada de anuncios.
 * @param  {string} url La URLConf donde hará la petición ajax.
 */
function initSearchAdvancedMap (url) {
  const urlConf = url;

  $(document).ready(function () {
    // Carga el mapa en modal.
    $('.btn-map-modal').on('click', function () {
      loadGoogleMap('map');
    });

    // Carga mapa en large.
    loadGoogleMap('map-large');
  });

  /**
   * Carga el mapa en el 'element'
   * @param  {string} element  Elemento donde cargara el 'map'.
   */
  function loadGoogleMap (element) {
    // obtenido de  src/static/src/js/geolocation.js
    const latitude = userLatitude;
    // obtenido de  src/static/src/js/geolocation.js
    const longitude = userLongitude;
    const background = '#1E90FF';
    const zoom = 14;
    // default 1.5 kilometros
    const radius = 1500;

    let map;
    let latLng;
    let circle;
    let markers = [];

    latLng = new google.maps.LatLng(latitude, longitude);
    map = new google.maps.Map(document.getElementById(element), {
      zoom: zoom,
      center: latLng,
      mapTypeId: google.maps.MapTypeId.ROADMAP,
      disableDefaultUI: true,
      zoomControl: true
    });

    circle = new google.maps.Circle({
      strokeColor: background,
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillColor: background,
      fillOpacity: 0.03,
      map: map,
      center: latLng,
      radius: radius,
      editable: true
    });

    // Mover circulo al centro del mapa.
    google.maps.event.addListener(map, 'dragend', function () {
      circle.setCenter(map.getCenter());
    });

    // Actualizar busqueda.
    google.maps.event.addListener(circle, 'radius_changed', getMarkersInCurrentPosition);
    google.maps.event.addListener(circle, 'center_changed', function () {
      map.setCenter(circle.getCenter());
      getMarkersInCurrentPosition();
      // Actualizar latitude y longitude en el form.
      updateLatLngInForm();
    });

    function getMarkersInCurrentPosition () {
      // Elementos del formulario.
      const latitude = circle.getCenter().lat();
      const longitude = circle.getCenter().lng();

      /**
       * Valores checked del formulario.
       * @param  {string} key #id del input.
       * @return {string} 'on' si el elemento esta marcado, '' en caso
       * contrario.
       */
      function checkboxValue (key) {
        if ($(key).is(':checked')) {
          return 'on';
        }
        return '';
      }

      const category = $('#id_category').val();
      const typeAnuncio = $('#id_type_anuncio').val();
      const metrosCuadrados = $('#id_metros_cuadrados').val();
      const habitaciones = $('#id_habitaciones').val();
      const banos = $('#id_banos').val();
      const precio = $('#id_precio').val();
      const genero = $('#id_genero').val();
      const internet = checkboxValue('#id_internet');
      const permiteFumarHabitacion = checkboxValue('#id_permite_fumar_habitacion');
      const permiteFumarPiso = checkboxValue('#id_permite_fumar_piso');

      $.ajax({
        url: urlConf,
        type: 'GET',
        dataType: 'json',
        data: {
          latitude: latitude,
          longitude: longitude,
          radius: circle.getRadius(),
          category: category,
          type_anuncio: typeAnuncio,
          metros_cuadrados: metrosCuadrados,
          habitaciones: habitaciones,
          banos: banos,
          precio: precio,
          genero: genero,
          internet: internet,
          permite_fumar_habitacion: permiteFumarHabitacion,
          permite_fumar_piso: permiteFumarPiso
        },
        success (data) {
          let fields;
          let latLng;
          let marker;
          let infoWindow;
          let currentInfoWindow;
          let content;

          // Eliminar todos los markers.
          if (markers.length > 0) {
            for (let k = 0; k < markers.length; k++) {
              markers[k].setMap(null);
            }
            markers = [];
          }

          function getRandomThumbnail (imageAnuncio) {
            let imagesCount = imageAnuncio.length;
            let urlImage;
            let number;
            if (!imagesCount) {
              urlImage = '/media/dummy-image.jpg';
            } else {
              number = Math.floor(Math.random() * (0, imagesCount - 1));
              urlImage = imageAnuncio[number].image;
            }
            return `<img class="z-depth-2 rounded"
                         src="${urlImage}"
                         alt="Imagen"
                         width="200"
                         height="150">`;
          }

          for (let i = 0; i < data.length; i++) {
            fields = data[i];
            latLng = new google.maps.LatLng(fields.latitude, fields.longitude);
            infoWindow = new google.maps.InfoWindow({});

            // Contenido del infoWindow.
            content =
              `<div class="infoWindow">
                <table class="table">
                  <thead>
                    <tr>
                      <th colspan="3">${fields.location_string}</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>
                        <span class="d-none d-lg-block">
                          ${getRandomThumbnail(fields.image_anuncio)}
                        </span>
                      </td>
                      <td>Precio</td>
                      <td>${fields.precio} ${fields.currency}</td>
                    </tr>
                  </tbody>
                </table>

                <div class="text-center">
                  <a class="btn btn-outline-primary btn-sm" href="/anuncios/details/${fields.pk}/">
                    Ver
                  </a>
                </div>
              </div>`;

            marker = new google.maps.Marker({
              position: latLng,
              map: map,
              title: fields.location_string,
              // http://www.codeshare.co.uk/blog/how-to-style-the-google-maps-popup-infowindow/
              icon: '/static/dist/img/blue-pin.png'
            });

            google.maps.event.addListener(marker, 'click', ((marker, content, infoWindow) => {
              return () => {
                if (currentInfoWindow) {
                  currentInfoWindow.close();
                }
                infoWindow.setContent(content);
                infoWindow.open(map, marker);
                currentInfoWindow = infoWindow;
              };
            })(marker, content, infoWindow));

            markers.push(marker);
          }

          // Mostrar numero de markers en dev.
          const bgcolor = (markers.length > 0) ? 'bg-success text-white' : 'bg-danger text-white';
          $('#search-advanced-results').html(
            `<div class="text-center ${bgcolor}" style="padding: 0.5rem;">
              Resultados encontrados <span class="badge badge-default">${markers.length}</span>
            </div>`
          );
        }
      });
    }

    // Inicializa la zona cuando carga la pagina.
    getMarkersInCurrentPosition();

    /**
     * Actualiza la búsqueda si cambia un valor del formulario.
     * @param {str} key ID elemento.
     */
    function updateElementForm (key) {
      if ($(key).length) {
        $(key).on('change keyup', function () {
          getMarkersInCurrentPosition();
        });
      }
    }

    updateElementForm('#id_type_anuncio');
    updateElementForm('#id_metros_cuadrados');
    updateElementForm('#id_habitaciones');
    updateElementForm('#id_banos');
    updateElementForm('#id_precio');
    updateElementForm('#id_permite_fumar_piso');
    updateElementForm('#id_genero');
    updateElementForm('#id_permite_fumar_habitacion');
    updateElementForm('#id_internet');
    /**
     * END Actualiza la búsqueda si cambia un valor del formulario.
     */

    /**
     * Actualiza en el form la latitud y la longitude.
     * Actualiza en localStorage la latitud y longitude.
     *
     * Así se recordara su posición en la que esta buscando.
     */
    function updateLatLngInForm () {
      const latitude = map.getCenter().lat();
      const longitude = map.getCenter().lng();

      // Actualizar los campos del formulario.
      latitudeInput.value = latitude;
      longitudeInput.value = longitude;

      // Actualizar localStorage.
      localStorage.setItem('latitude', latitude);
      localStorage.setItem('longitude', longitude);

      // Actualizar userLatitude y userLongitude.
      userLatitude = latitude; // eslint-disable-line
      userLongitude = longitude; // eslint-disable-line
    }

    /**
     * Recarga el mapa en el lienzo.
     */
    function reloadMap () {
      const lastCenter = map.getCenter();
      const lastZoom = map.getZoom();
      google.maps.event.trigger(map, 'resize');
      map.setCenter(lastCenter);
      map.setZoom(lastZoom);
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
}
