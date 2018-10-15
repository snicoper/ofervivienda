/*global userLatitude, userLongitude, polygonCenter*/
/**
 * Algunas Fuentes:
 * http://stackoverflow.com/questions/14166546/google-maps-drawing-manager-limit-to-1-polygon
 * http://stackoverflow.com/questions/12004550/how-to-delete-all-the-shape-after-draw
 * http://stackoverflow.com/questions/28110795/google-maps-draw-polygon-and-delete-the-previous-one
 * https://developers.google.com/maps/documentation/javascript/shapes#dragging_events
 * https://developers.google.com/maps/documentation/javascript/drawinglayer?hl=es-419
 */
/**
 * Carga el mapa con un polígono para ver o dibujar.
 * @param  {bool} editable Editable la forma?
 */
function initShapeMap (editable) {
  $(document).ready(function () {
    // Carga el mapa en modal.
    $('.btn-map-modal').on('click', function () {
      loadGoogleMap('map', editable);
    });

    // Carga mapa en large.
    loadGoogleMap('map-large', editable);
  });

  /**
   * Carga el mapa en el 'element'
   * @param  {string} element  Elemento donde cargara el 'map'.
   * @param  {bool} editable ¿El mapa es editable?
   */
  function loadGoogleMap (element, editable) {
    let map;
    let drawingManager;
    let shapes = [];
    let polygon;
    const background = '#1E90FF';

    // obtenido de  src/static/src/js/geolocation.js
    const latitude = userLatitude;

    // obtenido de  src/static/src/js/geolocation.js
    const longitude = userLongitude;

    const polygonInput = document.getElementById('id_polygon');
    let coords;
    let latLng;
    let zoom = 10;

    if (polygonInput.value) {
      zoom = 14;
    }

    latLng = new google.maps.LatLng(latitude, longitude);
    map = new google.maps.Map(document.getElementById(element), {
      zoom: zoom,
      center: latLng,
      mapTypeId: google.maps.MapTypeId.ROADMAP,
      disableDefaultUI: true,
      zoomControl: true
    });

    if (editable === true) {
      const polyOptions = {
        strokeWeight: 0,
        fillOpacity: 0.45,
        editable: editable,
        strokeColor: background,
        fillColor: background,
        draggable: editable
      };

      // Creates a drawing manager attached to the map that allows the user to
      // draw markers, lines, and shapes.
      drawingManager = new google.maps.drawing.DrawingManager({
        drawingMode: google.maps.drawing.OverlayType.POLYGON,
        drawingControlOptions: {
          drawingModes: [
            google.maps.drawing.OverlayType.POLYGON
          ]
        },
        rectangleOptions: polyOptions,
        circleOptions: polyOptions,
        polygonOptions: polyOptions,
        map: map
      });

      // Add a listener for creating new shape event.
      google.maps.event.addListener(drawingManager, 'overlaycomplete', (event) => {
        const newShape = event.overlay;
        newShape.type = event.type;
        shapes.push(newShape);
        coordsToFormField(newShape);

        if (drawingManager.getDrawingMode()) {
          drawingManager.setDrawingMode(null);
        }

        // Posicionar el mapa en el centro.
        map.setCenter(polygonCenter(newShape));
      });

      // add a listener for the drawing mode change event, delete any existing
      // polygons
      google.maps.event.addListener(drawingManager, 'drawingmode_changed', () => {
        if (drawingManager.getDrawingMode() !== null) {
          for (let i = 0; i < shapes.length; i++) {
            shapes[i].setMap(null);
          }
          shapes = [];
        }
      });
    }

    // Si el form tiene coords, obtener coords y dibujarlas.
    if (polygonInput.value) {
      coords = formFieldToCoords();

      polygon = new google.maps.Polygon({
        map: map,
        paths: coords,
        strokeWeight: 0,
        fillOpacity: 0.45,
        editable: editable,
        strokeColor: background,
        fillColor: background,
        draggable: editable
      });

      // Desactivar la edición del polígono.
      if (drawingManager) {
        drawingManager.setDrawingMode(null);

        // Si cambia drawingmode, eliminar el polygon object.
        google.maps.event.addListener(drawingManager, 'drawingmode_changed', () => {
          // Si polygon existe, tambien lo eliminamos.
          if (polygon) {
            polygon.setMap(null);
          }
        });
      }

      // Posicionar el mapa en el centro.
      map.setCenter(polygonCenter(polygon));

      // Events, cualquier movimiento de los puntos o la geometría.
      google.maps.event.addListener(polygon, 'click', () => {
        coordsToFormField(polygon);
      });
      google.maps.event.addListener(polygon, 'dragend', () => {
        coordsToFormField(polygon);

        // Posicionar el mapa en el centro.
        map.setCenter(polygonCenter(polygon));
      });
      google.maps.event.addListener(polygon.getPath(), 'insert_at', () => {
        coordsToFormField(polygon);

        // Posicionar el mapa en el centro.
        map.setCenter(polygonCenter(polygon));
      });
      google.maps.event.addListener(polygon.getPath(), 'set_at', () => {
        coordsToFormField(polygon);

        // Posicionar el mapa en el centro.
        // DESACTIVADO: Se hace incomodo al entrar en "conflicto" con el evento
        // dragend. cuando se mueve el poligono, representa que cambian todos
        // los vertices y activa este evento constantemente.
        // map.setCenter(polygonCenter(polygon));
      });
    }

    /**
    * Construir el string POLYGON para Django y añadirlo
    * al campo del formulario.
    */
    function coordsToFormField (polygon) {
      // Total coords.
      const len = polygon.getPath().getLength();
      // Coords guardadas en un array.
      let coordsPolygon = [];
      // Variables temporales para el for.
      let coords;
      let latitude = '';
      let longitude = '';
      for (let i = 0; i < len; i++) {
        coords = polygon.getPath().getAt(i).toUrlValue(5).split(',');
        latitude = coords[0];
        longitude = coords[1];
        coordsPolygon.push(longitude + ' ' + latitude);
      }

      // Actualizar campos en el form a una de las coords.
      document.getElementById('id_latitude').value = latitude;
      document.getElementById('id_longitude').value = longitude;

      // La ultima coordenada, ha de ser igual a la primera, para cerrar.
      polygonInput.value = 'POLYGON ((' + coordsPolygon.join(', ') + ', ' + coordsPolygon[0] + '))';
    }

    /**
     * Obtiene del form el string GEOSGeometry.
     * Separa las coordenadas en un array para construir el polygon.
     *
     * @return {array} Coordenadas para paths.
     */
    function formFieldToCoords () {
      // obtener el valor entre 'POLYGON ((' y '))'
      const regex = /POLYGON \(\((.*)\)\)/;
      const coords = regex.exec(polygonInput.value)[1];

      let pathsPolygons = [];
      let lat;
      let lng;
      let splitParts;
      let parts = coords.split(', ');

      parts.pop();
      for (let i = 0; i < parts.length; i++) {
        splitParts = parts[i].split(' ');
        lat = parseFloat(splitParts[1]);
        lng = parseFloat(splitParts[0]);
        pathsPolygons.push(new google.maps.LatLng(lat, lng));
      }

      return pathsPolygons;
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
