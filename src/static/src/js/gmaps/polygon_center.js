/**
 * Centra el mapa segun el poligono.
 *
 * https://gist.github.com/jeremejazz/9407568
 *
 * @param  {polygon} poly Poligono de maps.
 * @return {google.maps.LatLng} Objeto LatLng.
 */
function polygonCenter (poly) {
  const vertices = poly.getPath();
  let lowx;
  let highx;
  let lowy;
  let highy;
  let lats = [];
  let lngs = [];
  let centerX;
  let centerY;

  for (let i = 0; i < vertices.length; i++) {
    lngs.push(vertices.getAt(i).lng());
    lats.push(vertices.getAt(i).lat());
  }

  lats.sort();
  lngs.sort();
  lowx = lats[0];
  highx = lats[vertices.length - 1];
  lowy = lngs[0];
  highy = lngs[vertices.length - 1];
  centerX = lowx + ((highx - lowx) / 2);
  centerY = lowy + ((highy - lowy) / 2);
  return (new google.maps.LatLng(centerX, centerY));
}
